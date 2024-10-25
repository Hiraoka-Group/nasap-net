from recsa import Assembly

__all__ = ['union_assemblies']


def union_assemblies(
        assembly1: Assembly, assembly2: Assembly,
        rename_prefix1: str | None = None,
        rename_prefix2: str | None = None
        ) -> Assembly:
    """Union two assemblies."""
    if rename_prefix1 is not None:
        rename_map1 = {
            comp_id: f'{rename_prefix1}{comp_id}'
            for comp_id in assembly1.component_ids}
        assembly1 = assembly1.rename_component_ids(rename_map1)

    if rename_prefix2 is not None:
        rename_map2 = {
            comp_id: f'{rename_prefix2}{comp_id}'
            for comp_id in assembly2.component_ids}
        assembly2 = assembly2.rename_component_ids(rename_map2)

    if set(assembly1.component_ids) & set(assembly2.component_ids):
        raise ValueError('The assemblies have overlapping component IDs.')

    duplicate_kinds = (
        assembly1.comp_kind_to_structure.keys()
        & assembly2.comp_kind_to_structure.keys())
    for kind in duplicate_kinds:
        if assembly1.comp_kind_to_structure[kind] != assembly2.comp_kind_to_structure[kind]:
            raise ValueError(
                f'The assemblies have different structures for component '
                f'kind "{kind}".')
    
    comp_kind_to_structure = (
        assembly1.comp_kind_to_structure
        | assembly2.comp_kind_to_structure)
    component_id_to_kind = (
        assembly1.component_id_to_kind | assembly2.component_id_to_kind)
    bonds = assembly1.bonds | assembly2.bonds

    return Assembly(
        comp_kind_to_structure, component_id_to_kind, bonds)
