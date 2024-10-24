from collections.abc import Mapping
from itertools import combinations

from networkx.utils import UnionFind, groups

from recsa import Assembly, Component
from recsa.algorithms.isomorphism import isomorphisms_iter

__all__ = ['compute_bindsite_equivalence_as_uf']


def compute_bindsite_equivalence_as_uf(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
        ) -> dict[str, UnionFind]:
    """Compute node equivalences of an assembly.

    Nodes in an assembly can be grouped into equivalence classes.
    Two nodes are in the same equivalence class if there exists at least
    one isomorphism between the assembly and itself that maps one node
    to the other.

    Parameters
    ----------
    assembly : Assembly
        The assembly.
    component_structures : Mapping[str, ComponentStructure]
        The component structures.

    Returns
    -------
    dict[str, UnionFind]
        A dictionary mapping component kinds to UnionFind objects.
        Each UnionFind object represents the equivalence classes of
        nodes of a component kind.
    """
    component_kind_to_uf = {
        kind: UnionFind(
            assembly.get_all_bindsites_of_kind(
                kind, component_structures))
        for kind in assembly.component_kinds
    }
    # Possibly more efficient algorithm can be used
    # in cases where the assembly has no auxiliary edges.

    for isomorphism in isomorphisms_iter(
            assembly, assembly, component_structures):
        for kind, uf in component_kind_to_uf.items():
            while _update_bindsite_equivalence(uf, isomorphism):
                pass

    return component_kind_to_uf


def _update_bindsite_equivalence(
        uf: UnionFind, isomorphism: Mapping[str, str]) -> bool:
    """Update the equivalence classes of nodes in an assembly
    based on a new isomorphism."""
    roots = set(uf[n] for n in uf)
    for root1, root2 in combinations(roots, 2):
        group1 = groups(uf.parents)[root1]
        group2 = groups(uf.parents)[root2]
        if any(isomorphism[n1] in group2 for n1 in group1):
            uf.union(root1, root2)
            return True
        if any(isomorphism[n2] in group1 for n2 in group2):
            uf.union(root1, root2)
            return True
    return False
