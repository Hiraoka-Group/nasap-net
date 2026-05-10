from nasap_net.helpers import union_assemblies
from nasap_net.models import Assembly, BindingSite, Bond, Component
from nasap_net.types import ID


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
