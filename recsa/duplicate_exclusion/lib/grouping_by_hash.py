from collections import defaultdict
from collections.abc import Mapping

from recsa import Assembly, ComponentStructure, calc_wl_hash_of_assembly

__all__ = ['group_assemblies_by_hash']

def group_assemblies_by_hash(
        id_to_assembly: Mapping[str, Assembly],
        component_structures: Mapping[str, ComponentStructure]
        ) -> dict[str, set[str]]:
    # Group by hash
    hash_to_ids = defaultdict(set)
    for id_, assembly in id_to_assembly.items():
        hash_ = calc_wl_hash_of_assembly(assembly, component_structures)
        hash_to_ids[hash_].add(id_)
    return hash_to_ids
