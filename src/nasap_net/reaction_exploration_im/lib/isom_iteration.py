from collections.abc import Iterator, Mapping

from networkx.algorithms.isomorphism import (GraphMatcher,
                                             categorical_edge_match,
                                             categorical_node_match)

from .assembly_to_graph import convert_assembly_to_graph
from ..models import Assembly, BindingSite


def iter_isomorphisms(
        assem1: Assembly, assem2: Assembly
        ) -> Iterator[Mapping[BindingSite, BindingSite]]:
    """Find all isomorphisms between two "g_snapshot" graphs of assemblies."""
    g1 = convert_assembly_to_graph(assem1)
    g2 = convert_assembly_to_graph(assem2)

    node_match = categorical_node_match('isom_key', None)
    edge_match = categorical_edge_match('aux_kind', None)
    matcher = GraphMatcher(
        g1, g2, node_match=node_match, edge_match=edge_match)
    for isom in matcher.isomorphisms_iter():
        yield {
            orig: mapped for orig, mapped in isom.items()
            if isinstance(orig, BindingSite)\
               and isinstance(mapped, BindingSite)
            }
