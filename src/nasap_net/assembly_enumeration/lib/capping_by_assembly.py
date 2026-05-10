from collections.abc import Iterable

from nasap_net.assembly_equivalence import extract_unique_assemblies
from nasap_net.helpers import union_assemblies
from nasap_net.models import Assembly, BindingSite, Bond, Component
from nasap_net.types import ID

from .capping import get_free_metal_sites


def cap_assemblies_with_assembly(
        assemblies: Iterable[Assembly],
        capping_assembly: Assembly,
        capping_assembly_site: BindingSite,
        metal_kinds: Iterable[str],
        *,
        return_only_unique: bool = True,
) -> set[Assembly]:
    result = {
        _cap_assembly_with_assembly(
            assembly=assembly,
            capping_assembly=capping_assembly,
            capping_assembly_site=capping_assembly_site,
            metal_kinds=metal_kinds,
        )
        for assembly in assemblies
    }
    if return_only_unique:
        return extract_unique_assemblies(result)
    return result


def _cap_assembly_with_assembly(
        assembly: Assembly,
        capping_assembly: Assembly,
        capping_assembly_site: BindingSite,
        metal_kinds: Iterable[str],
) -> Assembly:
    free_metal_sites = sorted(get_free_metal_sites(assembly, metal_kinds))
    for i, site in enumerate(free_metal_sites):
        assembly = _attach_assembly(
            assembly=assembly,
            assembly_site=site,
            capping_assembly=capping_assembly,
            capping_assembly_site=capping_assembly_site,
            id_prefix=f'cap{i}_',
        )
    return assembly


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
        capping_assembly: Assembly,
        capping_assembly_site: BindingSite,
        id_prefix: str,
) -> Assembly:
    renamed = _rename_assembly(capping_assembly, id_prefix)
    renamed_site = BindingSite(
        f'{id_prefix}{capping_assembly_site.component_id}',
        capping_assembly_site.site_id,
    )
    return union_assemblies(assembly, renamed).add_bond(assembly_site, renamed_site)
