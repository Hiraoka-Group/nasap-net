from collections.abc import Iterable
from itertools import combinations

from nasap_net.assembly_equivalence import extract_unique_assemblies
from nasap_net.models import Assembly, BindingSite

from .substitution_with_assembly import _attach_assembly


def enumerate_assemblies_capped_with_assembly(
        assemblies: Iterable[Assembly],
        component_kind: str,
        capping_assembly: Assembly,
        capping_assembly_site: BindingSite,
) -> set[Assembly]:
    result: set[Assembly] = set()
    for assembly in assemblies:
        result.update(_enumerate_capped(
            assembly=assembly,
            component_kind=component_kind,
            capping_assembly=capping_assembly,
            capping_assembly_site=capping_assembly_site,
        ))
    return extract_unique_assemblies(result)


def _enumerate_capped(
        assembly: Assembly,
        component_kind: str,
        capping_assembly: Assembly,
        capping_assembly_site: BindingSite,
) -> set[Assembly]:
    free_sites = list(assembly.find_sites(has_bond=False, component_kind=component_kind))

    result: set[Assembly] = set()
    for r in range(1, len(free_sites) + 1):
        for subset in combinations(free_sites, r):
            result.add(_cap_sites(
                assembly=assembly,
                sites=list(subset),
                capping_assembly=capping_assembly,
                capping_assembly_site=capping_assembly_site,
            ))
    return result


def _cap_sites(
        assembly: Assembly,
        sites: list[BindingSite],
        capping_assembly: Assembly,
        capping_assembly_site: BindingSite,
) -> Assembly:
    for i, site in enumerate(sites):
        assembly = _attach_assembly(
            assembly=assembly,
            assembly_site=site,
            substituting_assembly=capping_assembly,
            substituting_assembly_site=capping_assembly_site,
            id_prefix=f'cap{i}_',
        )
    return assembly
