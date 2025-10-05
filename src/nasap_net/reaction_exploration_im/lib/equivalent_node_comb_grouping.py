from collections.abc import Iterable, Mapping

from .union_find import UnionFind
from ..models import BindingSite


def group_equivalent_node_combs(
        node_combs: Iterable[tuple[BindingSite, ...]],
        isomorphisms: Iterable[Mapping[BindingSite, BindingSite]]
        ) -> list[set[tuple[BindingSite, ...]]]:
    """Group equivalent node combinations."""
    node_combs = set(node_combs)
    uf = UnionFind(node_combs)
    for isom in isomorphisms:
        for comb in node_combs:
            mapped_comb = tuple(isom[site] for site in comb)
            if mapped_comb in node_combs:
                uf.union(comb, mapped_comb)
    return [
        set(elements) for elements
        in uf.root_to_elements.values()]
