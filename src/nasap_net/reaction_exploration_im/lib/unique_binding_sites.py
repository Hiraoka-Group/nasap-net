from collections.abc import Iterable
from dataclasses import dataclass

from .equivalent_node_comb_grouping import group_equivalent_node_combs
from .igraph import get_all_isomorphisms
from ..models import Assembly, BindingSite


@dataclass(frozen=True)
class UniqueComb:
    """A unique binding site or binding site set with duplication count."""
    site_comb: tuple[BindingSite, ...]
    duplication: int


def extract_unique_site_combinations(
        binding_site_combs: Iterable[tuple[BindingSite, ...]],
        assembly: Assembly,
        ) -> list[UniqueComb]:
    """Compute unique binding sites or binding site sets."""
    self_isomorphisms = get_all_isomorphisms(assembly, assembly)
    binding_site_isoms = [
        isom.binding_site_mapping for isom in self_isomorphisms]

    grouped_node_combs = group_equivalent_node_combs(
        binding_site_combs, binding_site_isoms)

    return [
        UniqueComb(
            site_comb=sorted(comb_group)[0],
            duplication=len(comb_group))
        for comb_group in grouped_node_combs
    ]
