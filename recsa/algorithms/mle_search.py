from collections.abc import Iterator, Mapping
from itertools import product

from recsa import Assembly, Component, MleBindsite, MleKind

__all__ = ['find_mles_by_kind']


def find_mles_by_kind(
        assembly: Assembly,
        mle_kind: MleKind,
        component_structures: Mapping[str, Component],
        ) -> Iterator[MleBindsite]:
    """Get all MLE bindsites of a specific kind.

    MLE bindsites are triples of metal, leaving, and entering bindsites.
    In a ligand exchange reaction, the bond between the metal and the
    leaving ligand is broken, and a bond between the metal and the entering
    ligand is formed.

    This function yields all triples of metal, leaving, and entering bindsites
    as MleBindsite objects. Yielded MLE satisfies the following conditions:
    - Each bindsite is of the corresponding kind.
    - The leaving bindsite is connected to a metal bindsite.
    - The entering bindsite is not connected to any bindsite.

    Yielded MLE bindsites may include "equivalent" MLE bindsites.
    To compute the equivalence, use compute_mle_equiv_for_specific_assembly.

    Parameters
    ----------
    assembly : Assembly
        The assembly.
    mle_kind : MleKind
        The component kinds of the MLE bindsites, 
        e.g., MleKind('M', 'L', 'X').
    component_structures : Mapping[str, ComponentStructure]
        The component structures.

    Yields
    ------
    MleBindsite
        The MLE bindsites, e.g., MleBindsite('M1.b', 'X1.a', 'L1.b').
    """
    entering_bindsites = assembly.get_all_bindsites_of_kind(
        mle_kind.entering, component_structures)
    not_connected_entering_bindsites = (
        bs for bs in entering_bindsites
        if assembly.get_connected_bindsite(bs) is None)
    leaving_bindsites = assembly.get_all_bindsites_of_kind(
        mle_kind.leaving, component_structures)
    connected_leaving_bindsites = (
        bs for bs in leaving_bindsites
        if assembly.get_connected_bindsite(bs) is not None)
    for entering, leaving in product(
            not_connected_entering_bindsites, connected_leaving_bindsites):
        metal = assembly.get_connected_bindsite(leaving)
        assert metal is not None
        if metal is not mle_kind.metal:
            yield MleBindsite(metal, leaving, entering)
