from collections.abc import Iterable
from functools import cached_property

import networkx as nx

from ..aux_edge import AuxEdge
from ..validations import (validate_name_of_binding_site,
                           validate_name_of_component_kind)
from .bindsite_existence_check import check_bindsites_of_aux_edges_exists

__all__ = ['Component']


class Component:
    """A component of an assembly. (Immutable)"""

    def __init__(
            self, 
            bindsites: Iterable[str],
            aux_edges: Iterable[AuxEdge] | None = None):
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

        if aux_edges is not None:
            self._aux_edges = frozenset(aux_edges)
        else:
            self._aux_edges = frozenset()
        check_bindsites_of_aux_edges_exists(
            self._aux_edges, self._bindsites)
    
    def __eq__(self, value: object) -> bool:
        if not isinstance(value, Component):
            return False
        return (
            self.bindsites == value.bindsites and
            self.aux_edges == value.aux_edges)

    @property
    def bindsites(self) -> frozenset[str]:
        return self._bindsites

    @property
    def aux_edges(self) -> frozenset[AuxEdge]:
        return self._aux_edges
