from collections.abc import Mapping

from networkx.utils import graphs_equal

from recsa import Assembly, Component

__all__ = ['assemblies_equal']


def assemblies_equal(
        assem1: Assembly, assem2: Assembly,
        ) -> bool:
    """Check if two assemblies are equal.

    Equality here means equal as Python objects, not isomorphism of the
    underlying graphs. Component names, binding site names, and the 
    auxiliary edge types must match.

    See Also
    --------
    recsa.is_isomorphic
    """
    return graphs_equal(assem1.graph, assem2.graph)
