from collections.abc import Iterable

from recsa import RecsaValueError

from ..aux_edge import AuxEdge

__all__ = ['check_bindsites_of_aux_edges_exists']


def check_bindsites_of_aux_edges_exists(
        aux_edges: Iterable[AuxEdge], binding_sites: Iterable[str]) -> None:
    """Check if the binding sites of the auxiliary edges exist in the
    binding sites of the component.
    """
    for aux_edge in aux_edges:
        for bindsite in aux_edge.bindsites:
            if bindsite not in binding_sites:
                raise RecsaValueError(
                    f'The binding site "{bindsite}" is not in '
                    f'the binding sites: {binding_sites}')
