from collections.abc import Iterable
from itertools import combinations

from nasap_net.assembly_equivalence import extract_unique_assemblies
from nasap_net.helpers import union_assemblies
from nasap_net.models import Assembly, BindingSite, Bond, Component
from nasap_net.types import ID


def enumerate_substitutions_with_assembly(
        assemblies: Iterable[Assembly],
        leaving_ligand_kind: str,
        substituting_assembly: Assembly,
        substituting_assembly_site: BindingSite,
) -> set[Assembly]:
    result: set[Assembly] = set()
    for assembly in assemblies:
        result.update(_enumerate_substitutions(
            assembly=assembly,
            leaving_ligand_kind=leaving_ligand_kind,
            substituting_assembly=substituting_assembly,
            substituting_assembly_site=substituting_assembly_site,
        ))
    return extract_unique_assemblies(result)


def _enumerate_substitutions(
        assembly: Assembly,
        leaving_ligand_kind: str,
        substituting_assembly: Assembly,
        substituting_assembly_site: BindingSite,
) -> set[Assembly]:
    leaving_ligand_ids = [
        comp_id
        for comp_id, comp in assembly.components.items()
        if comp.kind == leaving_ligand_kind
        and any(comp_id in bond.component_ids for bond in assembly.bonds)
    ]

    result: set[Assembly] = set()
    for r in range(1, len(leaving_ligand_ids) + 1):
        for subset in combinations(leaving_ligand_ids, r):
            result.add(_substitute_ligands(
                assembly=assembly,
                leaving_ligand_ids=list(subset),
                substituting_assembly=substituting_assembly,
                substituting_assembly_site=substituting_assembly_site,
            ))
    return result


def _substitute_ligands(
        assembly: Assembly,
        leaving_ligand_ids: list[ID],
        substituting_assembly: Assembly,
        substituting_assembly_site: BindingSite,
) -> Assembly:
    for i, ligand_id in enumerate(leaving_ligand_ids):
        assembly = _substitute_ligand(
            assembly=assembly,
            leaving_ligand_id=ligand_id,
            substituting_assembly=substituting_assembly,
            substituting_assembly_site=substituting_assembly_site,
            id_prefix=f'sub{i}_',
        )
    return assembly


def _substitute_ligand(
        assembly: Assembly,
        leaving_ligand_id: ID,
        substituting_assembly: Assembly,
        substituting_assembly_site: BindingSite,
        id_prefix: str,
) -> Assembly:
    ligand_bond = next(
        bond for bond in assembly.bonds
        if leaving_ligand_id in bond.component_ids
    )
    metal_site = next(
        site for site in ligand_bond.sites
        if site.component_id != leaving_ligand_id
    )
    stripped_components: dict[ID, Component] = {
        comp_id: comp
        for comp_id, comp in assembly.components.items()
        if comp_id != leaving_ligand_id
    }
    stripped_bonds = {bond for bond in assembly.bonds if bond != ligand_bond}
    stripped = Assembly(components=stripped_components, bonds=stripped_bonds)

    return _attach_assembly(
        assembly=stripped,
        assembly_site=metal_site,
        substituting_assembly=substituting_assembly,
        substituting_assembly_site=substituting_assembly_site,
        id_prefix=id_prefix,
    )


def _rename_assembly(assembly: Assembly, id_prefix: str) -> Assembly:
    renamed_components: dict[ID, Component] = {
        f'{id_prefix}{comp_id}': comp
        for comp_id, comp in assembly.components.items()
    }
    renamed_bonds = {
        Bond.from_sites(*[
            BindingSite(f'{id_prefix}{s.component_id}', s.site_id)
            for s in b.sites
        ])
        for b in assembly.bonds
    }
    return Assembly(components=renamed_components, bonds=renamed_bonds)


def _attach_assembly(
        assembly: Assembly,
        assembly_site: BindingSite,
        substituting_assembly: Assembly,
        substituting_assembly_site: BindingSite,
        id_prefix: str,
) -> Assembly:
    renamed = _rename_assembly(substituting_assembly, id_prefix)
    renamed_site = BindingSite(
        f'{id_prefix}{substituting_assembly_site.component_id}',
        substituting_assembly_site.site_id,
    )
    return union_assemblies(assembly, renamed).add_bond(assembly_site, renamed_site)
