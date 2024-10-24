from collections.abc import Mapping

from recsa import Assembly, Component
from recsa.algorithms.bindsite_equivalence.as_dict import \
    compute_bindsite_to_root_maps
from recsa.algorithms.bindsite_equivalence.typing import (AssemblyId,
                                                          BindsiteToRoot,
                                                          ComponentKind)

__all__ = [
    'compute_bindsite_to_root_maps_for_multi_assemblies',
    ]


def compute_bindsite_to_root_maps_for_multi_assemblies(
        id_to_assembly: Mapping[str, Assembly],
        component_structures: Mapping[str, Component]
        ) -> dict[tuple[AssemblyId, ComponentKind], BindsiteToRoot]:
    """Compute a mapping from bindsite to its root node.

    The root node is the smallest node in the equivalent node group.
    """
    d = {}
    for id_, assembly in id_to_assembly.items():
        comp_kind_to_map = compute_bindsite_to_root_maps(
            assembly, component_structures)
        for kind, bindsite_to_root in comp_kind_to_map.items():
            d[(id_, kind)] = bindsite_to_root
    return d
