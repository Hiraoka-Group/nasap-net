from collections.abc import Iterable

from nasap_net.utils import UnionFind
from .igraph import get_all_isomorphisms
from .. import Assembly
from ..models import BindingSite


def group_equivalent_node_combs(
        node_combs: Iterable[tuple[BindingSite, ...]],
        assembly: Assembly,
        ) -> set[frozenset[tuple[BindingSite, ...]]]:
    """Group equivalent node combinations."""
    node_combs = set(node_combs)
    uf = UnionFind(node_combs)

    self_isomorphisms = get_all_isomorphisms(assembly, assembly)
    binding_site_isoms = [
        isom.binding_site_mapping for isom in self_isomorphisms]

    for isom in binding_site_isoms:
        for comb in node_combs:
            mapped_comb = tuple(isom[site] for site in comb)
            if mapped_comb in node_combs:
                uf.union(comb, mapped_comb)
    return {
        frozenset(elements) for elements
        in uf.root_to_elements.values()}
