from collections.abc import Mapping

from recsa import Assembly, ComponentStructure

from .lib import group_assemblies_by_isomorphism

__all__ = ['exclude_remaining_duplicates']


def exclude_remaining_duplicates(
        id_to_assembly: Mapping[str, Assembly],
        component_structures: Mapping[str, ComponentStructure],
        ) -> tuple[dict[str, Assembly], dict[str, set[str]]]:
    """Exclude remaining duplicates."""
    unique_id_to_ids = group_assemblies_by_isomorphism(id_to_assembly, component_structures)
    unique_ids = unique_id_to_ids.keys()
    unique_assemblies = {id_: id_to_assembly[id_] for id_ in unique_ids}
    return unique_assemblies, unique_id_to_ids
