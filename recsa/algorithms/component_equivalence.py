from collections.abc import Mapping
from itertools import combinations

from networkx.utils import UnionFind, groups

from recsa import Assembly
from recsa.algorithms.isomorphism import rough_isomorphisms_iter

__all__ = ['compute_component_equivalence']


def compute_component_equivalence(assembly: Assembly) -> UnionFind:
    """Compute component equivalences of an assembly."""
    uf = UnionFind(assembly.component_ids)
    for isomorphism in rough_isomorphisms_iter(assembly, assembly):
        while _update_component_equivalence(uf, isomorphism):
            pass
    return uf


def _update_component_equivalence(
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
