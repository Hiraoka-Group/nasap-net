from collections.abc import Iterable
from functools import cached_property
from typing import cast

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
            aux_edges: (
                Iterable[AuxEdge] | Iterable[tuple[str, str, str]] | None
                ) = None):
        for bindsite in bindsites:
            validate_name_of_binding_site(bindsite)
        self._bindsites = frozenset(bindsites)

        if aux_edges is None or not aux_edges:
            self._aux_edges = frozenset[AuxEdge]()
        elif isinstance(next(iter(aux_edges)), AuxEdge):
            aux_edges = cast(Iterable[AuxEdge], aux_edges)
            self._aux_edges = frozenset(aux_edges)
        else:
            aux_edges = cast(Iterable[tuple[str, str, str]], aux_edges)
            self._aux_edges = frozenset(
                AuxEdge(*aux_edge) for aux_edge in aux_edges)

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
