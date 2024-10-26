from collections.abc import Iterable
from typing import cast

from ..aux_edge import AuxEdge
from ..validations import validate_name_of_binding_site
from .bindsite_existence_check import check_bindsites_of_aux_edges_exists

__all__ = ['Component']


class Component:
    """A component of an assembly. (Immutable)"""

    def __init__(
            self,
            bindsites: Iterable[str],
            aux_edges: (
                Iterable[AuxEdge] 
                | Iterable[tuple[str, str, str]] | None
                ) = None):
        """
        Parameters
        ----------
        component_kind : str
            The component type, e.g., 'M', 'L', 'L1', 'X', etc.
        binding_sites : Iterable[str]
            The binding sites. Each binding site should be a string.
        aux_edges : Mapping[tuple[str, str], str], optional
            Mapping of auxiliary edges. The keys are tuples of two binding
            sites, and the values are the auxiliary kinds. The binding sites
            should be in the binding_sites.
            Duplicate pairs of binding sites raise an error regardless of the
            order of the binding sites.
        """
        for bindsite in bindsites:
            validate_name_of_binding_site(bindsite)
        self._bindsites = frozenset(bindsites)

        if aux_edges is None:
            self._aux_edges = frozenset[AuxEdge]()
        elif all(isinstance(edge, AuxEdge) for edge in aux_edges):
            aux_edges = cast(Iterable[AuxEdge], aux_edges)
            self._aux_edges = frozenset(aux_edges)
        else:
            aux_edges = cast(Iterable[tuple[str, str, str]], aux_edges)
            self._aux_edges = frozenset(
                {AuxEdge(*edge) for edge in aux_edges})

        check_bindsites_of_aux_edges_exists(
            self._aux_edges, self._bindsites)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Component):
            return False
        return (
            self.bindsites == value.bindsites
            and self.aux_edges == value.aux_edges)
    
    @property
    def bindsites(self) -> set[str]:
        return set(self._bindsites)

    @property
    def aux_edges(self) -> set[AuxEdge]:
        return set(self._aux_edges)
