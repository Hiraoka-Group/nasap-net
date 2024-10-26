from collections.abc import Callable
from copy import deepcopy
from functools import wraps

import networkx as nx

from recsa import RecsaValueError

from ..aux_edge import AuxEdge
from ..validations import (validate_name_of_binding_site,
                           validate_name_of_component_kind)
from .bindsite_existence_check import check_bindsites_of_aux_edges_exists

__all__ = ['Component']


class Component:
    """A component of an assembly."""

    def __init__(
            self, component_kind: str, 
            binding_sites: set[str],
            aux_edges: set[AuxEdge] | None = None):
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
        validate_name_of_component_kind(component_kind)
        self.__component_kind = component_kind

        for bindsite in binding_sites:
            validate_name_of_binding_site(bindsite)
        self.__binding_sites = binding_sites.copy()

        self.__aux_edges = aux_edges or set()
        check_bindsites_of_aux_edges_exists(
            self.__aux_edges, self.__binding_sites)
        
        # The graph snapshot cache.
        self.__g_cache = None
    
    def __eq__(self, value: object) -> bool:
        return NotImplemented

    # Decorator
    @staticmethod
    def clear_g_cache(func: Callable):
        """Decorator to clear the cache of the graph snapshot before
        calling the method."""
        @wraps(func)
        def wrapper(self, *args, **kwargs):
            assert hasattr(self, '_Component__g_cache'), (
                'The "__g_cache" attribute is not found. '
                'Please make sure that the "__g_cache" attribute is '
                'initialized in the __init__ method.')
            self.__g_cache = None
            return func(self, *args, **kwargs)
        return wrapper
    
    @property
    def binding_sites(self) -> set[str]:
        return self.__binding_sites.copy()

    @property
    def aux_edges(self) -> set[AuxEdge]:
        # TODO: Consider not to make a deep copy. It's costly.
        return deepcopy(self.__aux_edges)
    
    @property
    def g_snapshot(self) -> nx.Graph:
        if self.__g_cache is None:
            self.__g_cache = self._to_graph()
        return deepcopy(self.__g_cache)

    @clear_g_cache
    def __add_binding_site(self, binding_site: str) -> None:
        """Add a binding site.
        
        Raises
        ------
        RecsaValueError
            If the binding site already exists.
        """
        validate_name_of_binding_site(binding_site)
        if binding_site in self.__binding_sites:
            raise RecsaValueError(
                f'The binding site "{binding_site}" already exists.')
        self.__binding_sites.add(binding_site)

    @clear_g_cache
    def __add_binding_sites(self, binding_sites: set[str]) -> None:
        """Add binding sites."""
        for bindsite in binding_sites:
            validate_name_of_binding_site(bindsite)
        for bindsite in binding_sites:
            if bindsite in self.__binding_sites:
                raise RecsaValueError(
                    f'The binding site "{bindsite}" already exists.')
        self.__binding_sites.update(binding_sites)

    @clear_g_cache
    def __remove_binding_site(self, binding_site: str) -> None:
        """Remove a binding site."""
        if binding_site not in self.__binding_sites:
            raise RecsaValueError(
                f'The binding site "{binding_site}" does not exist.')
        self.__binding_sites.remove(binding_site)

    @clear_g_cache
    def __remove_binding_sites(self, binding_sites: set[str]) -> None:
        """Remove binding sites."""
        for bindsite in binding_sites:
            self.__remove_binding_site(bindsite)

    @clear_g_cache
    def __add_aux_edge(self, aux_edge: AuxEdge) -> None:
        """Add an auxiliary edge."""
        if aux_edge in self.__aux_edges:
            raise RecsaValueError(
                f'The auxiliary edge "{aux_edge}" already exists.')
        for bindsite in aux_edge.bindsites:
            if bindsite not in self.__binding_sites:
                raise RecsaValueError(
                    f'The binding site "{bindsite}" is not in the binding sites.')
        self.__aux_edges.add(aux_edge)
    
    @clear_g_cache
    def __add_aux_edges(self, aux_edges: set[AuxEdge]) -> None:
        """Add auxiliary edges."""
        for aux_edge in aux_edges:
            self.__add_aux_edge(aux_edge)
    
    @clear_g_cache
    def __remove_aux_edge(self, aux_edge: AuxEdge) -> None:
        """Remove an auxiliary edge."""
        if aux_edge not in self.__aux_edges:
            raise RecsaValueError(
                f'The auxiliary edge "{aux_edge}" does not exist.')
        self.__aux_edges.remove(aux_edge)

    @clear_g_cache
    def __remove_aux_edges(self, aux_edges: set[AuxEdge]) -> None:
        """Remove auxiliary edges."""
        for aux_edge in aux_edges:
            self.__remove_aux_edge(aux_edge)

    def _to_graph(self) -> nx.Graph:
        G = nx.Graph()
        G.add_node(
            'core', core_or_bindsite='core',
            component_kind=self.component_kind)
        for bindsite in self.binding_sites:
            G.add_node(bindsite, core_or_bindsite='bindsite')
            G.add_edge('core', bindsite)
        for aux_edge in self.aux_edges:
            G.add_edge(*aux_edge.bindsites, aux_type=aux_edge.aux_type)
        return G
