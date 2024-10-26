from collections.abc import Iterable
from copy import deepcopy

from recsa import RecsaValueError

from ..aux_edge import AuxEdge
from ..validations import (validate_name_of_binding_site,
                           validate_name_of_component_kind)
from .bindsite_existence_check import check_bindsites_of_aux_edges_exists

__all__ = ['Component']


class Component:
    """A component of an assembly."""

    def __init__(
            self,
            binding_sites: Iterable[str],
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
        for bindsite in binding_sites:
            validate_name_of_binding_site(bindsite)
        self.__binding_sites = set(binding_sites)

        self.__aux_edges = aux_edges or set()
        check_bindsites_of_aux_edges_exists(
            self.__aux_edges, self.__binding_sites)
        
        # The graph snapshot cache.
        self.__g_cache = None
    
    def __eq__(self, value: object) -> bool:
        return NotImplemented
    
    @property
    def binding_sites(self) -> set[str]:
        return self.__binding_sites.copy()

    @property
    def aux_edges(self) -> set[AuxEdge]:
        # TODO: Consider not to make a deep copy. It's costly.
        return deepcopy(self.__aux_edges)

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

    def __add_binding_sites(self, binding_sites: set[str]) -> None:
        """Add binding sites."""
        for bindsite in binding_sites:
            validate_name_of_binding_site(bindsite)
        for bindsite in binding_sites:
            if bindsite in self.__binding_sites:
                raise RecsaValueError(
                    f'The binding site "{bindsite}" already exists.')
        self.__binding_sites.update(binding_sites)

    def __remove_binding_site(self, binding_site: str) -> None:
        """Remove a binding site."""
        if binding_site not in self.__binding_sites:
            raise RecsaValueError(
                f'The binding site "{binding_site}" does not exist.')
        self.__binding_sites.remove(binding_site)

    def __remove_binding_sites(self, binding_sites: set[str]) -> None:
        """Remove binding sites."""
        for bindsite in binding_sites:
            self.__remove_binding_site(bindsite)

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
    
    def __add_aux_edges(self, aux_edges: set[AuxEdge]) -> None:
        """Add auxiliary edges."""
        for aux_edge in aux_edges:
            self.__add_aux_edge(aux_edge)
    
    def __remove_aux_edge(self, aux_edge: AuxEdge) -> None:
        """Remove an auxiliary edge."""
        if aux_edge not in self.__aux_edges:
            raise RecsaValueError(
                f'The auxiliary edge "{aux_edge}" does not exist.')
        self.__aux_edges.remove(aux_edge)

    def __remove_aux_edges(self, aux_edges: set[AuxEdge]) -> None:
        """Remove auxiliary edges."""
        for aux_edge in aux_edges:
            self.__remove_aux_edge(aux_edge)
