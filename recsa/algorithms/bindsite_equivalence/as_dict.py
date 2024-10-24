from collections.abc import Mapping

from networkx.utils import UnionFind

from recsa import Assembly, Component

from .as_uf import compute_bindsite_equivalence_as_uf
from .typing import BindsiteToRoot, ComponentKind

__all__ = ['compute_bindsite_to_root_maps']


def compute_bindsite_to_root_maps(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        ) -> dict[ComponentKind, BindsiteToRoot]:
    """Compute node equivalences of an assembly.
    
    Parameters
    ----------
    assembly : Assembly
        The assembly.
    component_structures : Mapping[str, ComponentStructure]
        The component structures.

    Returns
    -------
    dict[str, BindsiteToRoot]
        A dictionary mapping component kinds to dictionaries.
        Each dictionary maps bindsites to their root nodes.
    """
    comp_kind_to_uf = compute_bindsite_equivalence_as_uf(
        assembly, component_structures)
    return {
        kind: _uf_to_map(uf)
        for kind, uf in comp_kind_to_uf.items()
    }


def _uf_to_map(uf: UnionFind) -> dict[str, str]:
    """Convert a UnionFind object to a dictionary."""
    bindsite_to_root = {}
    for group in uf.to_sets():
        root = min(group)
        for node in group:
            bindsite_to_root[node] = root
    return bindsite_to_root
