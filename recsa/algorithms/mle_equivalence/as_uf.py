from collections.abc import Iterable, Mapping
from itertools import combinations

from networkx.utils import UnionFind, groups

from recsa import Assembly, Component, MleKind
from recsa.algorithms.isomorphism import isomorphisms_iter
from recsa.algorithms.isomorphism_application_to_mle import \
    apply_isomorphism_to_mle
from recsa.algorithms.mle_search import find_mles_by_kind

__all__ = ['compute_mle_equivalence_as_uf']


def compute_mle_equivalence_as_uf(
        assembly: Assembly, mle_kinds: Iterable[MleKind],
        component_structures: Mapping[str, Component],
        ) -> dict[MleKind, UnionFind]:
    """Compute MLE bindsite equivalences and return them as UnionFind objects.

    Nodes in an assembly can be grouped into equivalence classes.
    Two nodes are in the same equivalence class if there exists at least
    one isomorphism between the assembly and itself that maps one node
    to the other.
    """
    mle_kind_to_uf = {
        mle_kind: UnionFind(find_mles_by_kind(
            assembly, mle_kind, component_structures))
        for mle_kind in mle_kinds}

    for isomorphism in isomorphisms_iter(
            assembly, assembly, component_structures):
        for mle_kind, uf in mle_kind_to_uf.items():
            while _update_mle_equivalence(uf, isomorphism):
                pass

    return mle_kind_to_uf


def _update_mle_equivalence(
        uf: UnionFind, isomorphism: Mapping[str, str]
        ) -> bool:
    """Update the equivalence classes of node pairs in an assembly
    based on a new isomorphism."""
    roots = set(uf[mle_bindsite] for mle_bindsite in uf)
    for root1, root2 in combinations(roots, 2):
        group1 = groups(uf.parents)[root1]
        group2 = groups(uf.parents)[root2]
        if any(
                apply_isomorphism_to_mle(mle_bindsite1, isomorphism)
                in group2 for mle_bindsite1 in group1):
            uf.union(root1, root2)
            return True
        if any(
                apply_isomorphism_to_mle(mle_bindsite2, isomorphism)
                in group1 for mle_bindsite2 in group2):
            uf.union(root1, root2)
            return True
    return False
