from __future__ import annotations

from collections.abc import Callable, Iterable, Iterator, Mapping
from copy import deepcopy
from dataclasses import dataclass
from functools import wraps
from itertools import chain
from types import MappingProxyType
from typing import Concatenate, Literal, ParamSpec, TypeVar, overload

import networkx as nx

from recsa import RecsaValueError

from .aux_edge import AuxEdge
from .component_structure import ComponentStructure

__all__ = ['Assembly', 'assembly_to_graph', 'assembly_to_rough_graph', 'find_free_bindsites']


# For type hint of the decorator
P = ParamSpec("P")
R = TypeVar("R")


@dataclass
class AbsAuxEdge:
    """An auxiliary edge specified by absolute binding sites."""
    bindsite1: str
    bindsite2: str
    aux_type: str


class Assembly:
    """A class to represent an assembly.
    
    An assembly is a group of components connected by bonds.
    """
    def __init__(
            self, 
            component_id_to_kind: Mapping[str, str] | None = None,
            bonds: Iterable[tuple[str, str] | frozenset[str]] | None = None,
            id_: str | None = None,
            ) -> None:
        """
        Parameters
        ----------
        component_id_to_kind : Mapping[str, str], optional
            The components of the assembly. The keys are the component IDs,
            and the values are the component kinds.
        bonds : Iterable[tuple[str, str]], optional
            The bonds between the components. Each bond is a tuple of two
            binding sites.
        """
        self.id = id_
        self.__components: dict[str, str] = {}
        self.__bonds: set[frozenset[str]] = set()
        self.__bindsite_to_connected: dict[str, str] = {}

        # NOTE: Make sure that the __rough_g_cache attributes
        # are initialized before calling any method that modifies the assembly.
        self.__rough_g_cache = None

        if component_id_to_kind is not None:
            for component_id, component_kind in component_id_to_kind.items():
                self.add_component(component_id, component_kind)
        if bonds is not None:
            for bindsite1, bindsite2 in bonds:
                self.add_bond(bindsite1, bindsite2)

    # Decorator
    # For type hint of the decorator, see the following link:
    # https://github.com/microsoft/pyright/issues/6472
    @staticmethod
    def clear_g_caches(func: Callable[Concatenate[Assembly, P], R]
            ) -> Callable[Concatenate[Assembly, P], R]:
        """Decorator to clear the cache of the graph snapshot before
        calling the method."""
        @wraps(func)
        def wrapper(self: Assembly, *args: P.args, **kwargs: P.kwargs):
            assert hasattr(self, '_Assembly__rough_g_cache'), (
                'The "__g_cache" attribute is not found. '
                'Please make sure that the "__rough_g_cache" attribute is '
                'initialized in the __init__ method.')
            self.__rough_g_cache = None
            return func(self, *args, **kwargs)
        return wrapper

    # ============================================================
    # Properties (read-only)
    # ============================================================

    @property
    def component_id_to_kind(self) -> MappingProxyType[str, str]:
        """Return a read-only view of the components.
        
        The returned object can be used like a dictionary, but it is
        read-only. Changes to the original assembly will be reflected
        in the returned object.
        """
        return MappingProxyType(self.__components.copy())
    
    @property
    def component_ids(self) -> set[str]:
        return set(self.__components.keys())

    @property
    def component_kinds(self) -> set[str]:
        return set(self.__components.values())
    
    @property
    def bonds(self) -> set[frozenset[str]]:
        return self.__bonds.copy()
    
    @property
    def bindsite_to_connected(self) -> MappingProxyType[str, str]:
        """Return a read-only view of the connected binding sites.
        
        Only the binding sites that are connected to other binding sites
        are included in the returned object.
        """
        return MappingProxyType(self.__bindsite_to_connected.copy())
    
    def g_snapshot(
            self, component_structures: Mapping[str, ComponentStructure]
            ) -> nx.Graph:
        """Returns a snapshot of the assembly graph.
        
        The snapshot is a deep copy of the assembly graph. Therefore,
        any modification to the snapshot will not affect the assembly.
        """
        # Prevent the user from modifying the assembly.
        return self._to_graph(component_structures)
    
    @property
    def rough_g_snapshot(self) -> nx.Graph:
        """Returns a rough graph of the assembly."""
        if self.__rough_g_cache is None:
            self.__rough_g_cache = self._to_rough_graph()
        return deepcopy(self.__rough_g_cache)
    
    # ============================================================
    # Methods to modify the assembly (using relative names)
    # ============================================================
    
    @clear_g_caches
    def add_component(
            self, component_id: str, component_kind: str) -> None:
        """Add a component to the assembly.
        
        Note: No bond is added between the component and the assembly.
        The user should add bonds between the component and the assembly
        if necessary.
        """
        self.__components[component_id] = component_kind

    @clear_g_caches
    def remove_component(self, component_id: str) -> None:
        del self.__components[component_id]
    
    @clear_g_caches
    def add_bond(self, bindsite1: str, bindsite2: str) -> None:
        """Add a bond to the assembly."""
        comp1, rel1 = Assembly.abs_to_rel(bindsite1)
        comp2, rel2 = Assembly.abs_to_rel(bindsite2)
        for comp in [comp1, comp2]:
            if comp not in self.__components:
                raise RecsaValueError(
                    f'The component "{comp}" does not exist in the assembly.')
        self.__bonds.add(frozenset([bindsite1, bindsite2]))
        self.__bindsite_to_connected[bindsite1] = bindsite2
        self.__bindsite_to_connected[bindsite2] = bindsite1

    @clear_g_caches
    def remove_bond(
            self, bindsite1: str, bindsite2: str) -> None:
        """Remove a bond from the assembly."""
        self.__bonds.remove(frozenset([bindsite1, bindsite2]))
        del self.__bindsite_to_connected[bindsite1]
        del self.__bindsite_to_connected[bindsite2]

    # ============================================================
    # Methods to make multiple modifications at once
    # ============================================================

    def add_components(self, components: Iterable[tuple[str, str]]) -> None:
        for component_id, component_kind in components:
            self.add_component(component_id, component_kind)

    def remove_components(self, component_ids: Iterable[str]) -> None:
        for component_id in component_ids:
            self.remove_component(component_id)

    def add_bonds(
            self, bonds: Iterable[tuple[str, str]]) -> None:
        for bindsite1, bindsite2 in bonds:
            self.add_bond(bindsite1, bindsite2)

    def remove_bonds(
            self, bonds: Iterable[tuple[str, str]]) -> None:
        for bindsite1, bindsite2 in bonds:
            self.remove_bond(bindsite1, bindsite2)
    
    # ============================================================
    # Methods to relabel the assembly
    # ============================================================
    
    # `@overload` decorator is just for type hinting;
    # it does not affect the behavior of the method.
    @overload
    @clear_g_caches
    def rename_component_ids(
            self, mapping: Mapping[str, str],
            *, copy: Literal[True] = True) -> Assembly:
        ...
    @overload
    @clear_g_caches
    def rename_component_ids(
            self, mapping: Mapping[str, str],
            *, copy: Literal[False]) -> None:
        ...
    @clear_g_caches
    def rename_component_ids(
            self, mapping: Mapping[str, str],
            *, copy: bool = True) -> Assembly | None:
        if copy:
            assem = deepcopy(self)
        else:
            assem = self

        new_components = {}
        for old_id, component in assem.__components.items():
            new_id = mapping.get(old_id, old_id)
            new_components[new_id] = component
        
        new_bonds = set()
        for bindsite1, bindsite2 in assem.__bonds:
            comp1, rel1 = Assembly.abs_to_rel(bindsite1)
            comp2, rel2 = Assembly.abs_to_rel(bindsite2)
            new_bindsite1 = Assembly.rel_to_abs(mapping.get(comp1, comp1), rel1)
            new_bindsite2 = Assembly.rel_to_abs(mapping.get(comp2, comp2), rel2)
            new_bonds.add(frozenset([new_bindsite1, new_bindsite2]))

        assem.__components = new_components
        assem.__bonds = new_bonds
        assem.__rough_g_cache = None

        # TODO: Check if the new component IDs are valid.
        
        return assem

    # ============================================================
    # Helper methods
    # ============================================================

    @overload
    def get_connected_bindsite(
            self, bindsite: str, error_if_free: Literal[False] = False
            ) -> str | None: ...
    @overload
    def get_connected_bindsite(
            self, bindsite: str, error_if_free: Literal[True]
            ) -> str: ...
    def get_connected_bindsite(
            self, bindsite, error_if_free=False):
        """Get the connected binding site of the binding site.
        
        Parameters
        ----------
        bindsite : str
            The binding site.
        error_if_free : bool, optional
            If True, raise an error if the binding site is free.
            It is useful when the user expects the binding site to be
            connected.

        Returns
        -------
        str | None
            The connected binding site. If the binding site is free,
            and `error_if_free` is False, return None.
        """
        connected = self.__bindsite_to_connected.get(bindsite)
        if connected is None and error_if_free:
            raise RecsaValueError(
                f'The binding site "{bindsite}" is free.')
        return connected
    
    def is_free_bindsite(self, bindsite: str) -> bool:
        return self.get_connected_bindsite(bindsite) is None
    
    def get_component_kind(self, component_id: str) -> str:
        return self.__components[component_id]
    
    def get_component_kind_of_core(self, core: str) -> str:
        comp_id, rel = Assembly.abs_to_rel(core)
        return self.get_component_kind(comp_id)
    
    def get_component_kind_of_bindsite(self, bindsite: str) -> str:
        comp_id, rel = Assembly.abs_to_rel(bindsite)
        return self.get_component_kind(comp_id)
    
    def deepcopy(self) -> Assembly:
        return deepcopy(self)
    
    def get_core_of_the_component(self, component_id: str) -> str:
        return Assembly.rel_to_abs(component_id, 'core')

    def iter_all_cores(self) -> Iterator[str]:
        for comp_id, comp_kind in self.component_id_to_kind.items():
            yield Assembly.rel_to_abs(comp_id, 'core')
    
    def get_all_bindsites(
            self, component_structures: Mapping[str, ComponentStructure]
            ) -> set[str]:
        """Get all the binding sites in the assembly."""
        # TODO: Consider yielding the binding sites instead of returning a set.
        all_bindsites = set()
        for comp_id, comp_kind in self.component_id_to_kind.items():
            comp_struct = component_structures[comp_kind]
            for bindsite in comp_struct.binding_sites:
                all_bindsites.add(Assembly.rel_to_abs(comp_id, bindsite))
        return all_bindsites

    def iter_aux_edges(
            self, component_structures: Mapping[str, ComponentStructure]
            ) -> Iterator[AbsAuxEdge]:
        for comp_id, comp_kind in self.component_id_to_kind.items():
            comp_struct = component_structures[comp_kind]
            for rel_aux_edge in comp_struct.aux_edges:
                yield AbsAuxEdge(
                    Assembly.rel_to_abs(comp_id, rel_aux_edge.bindsite1),
                    Assembly.rel_to_abs(comp_id, rel_aux_edge.bindsite2),
                    rel_aux_edge.aux_type)

    def get_bindsites_of_component(
            self, component_id: str, 
            component_structures: Mapping[str, ComponentStructure]
            ) -> set[str]:
        """Get the binding sites of the component."""
        comp_kind = self.get_component_kind(component_id)
        comp_struct = component_structures[comp_kind]
        return {
            Assembly.rel_to_abs(component_id, bindsite)
            for bindsite in comp_struct.binding_sites}
    
    def get_all_bindsites_of_kind(
            self, component_kind: str,
            component_structures: Mapping[str, ComponentStructure],
            ) -> Iterator[str]:
        for comp_id, comp in self.component_id_to_kind.items():
            if comp == component_kind:
                yield from self.get_bindsites_of_component(
                    comp_id, component_structures)

    def find_free_bindsites(
            self, component_structures: Mapping[str, ComponentStructure]
            ) -> set[str]:
        """Find free bindsites."""
        all_bindsites = {
            Assembly.rel_to_abs(comp_id, bindsite)
            for comp_id, comp_kind in self.component_id_to_kind.items()
            for bindsite in component_structures[comp_kind].binding_sites
        }
        connected_bindsites = chain(*self.bonds)
        free_bindsites = all_bindsites - set(connected_bindsites)
        return free_bindsites

    # ============================================================
    # Methods to convert the assembly to graphs
    # ============================================================

    def _to_graph(
            self, component_kinds: Mapping[str, ComponentStructure]
            ) -> nx.Graph:
        return assembly_to_graph(self, component_kinds)

    def _to_rough_graph(self) -> nx.Graph:
        G = nx.Graph()
        for comp_id, comp_kind in self.component_id_to_kind.items():
            G.add_node(comp_id, component_kind=comp_kind)
        for bindsite1, bindsite2 in self.bonds:
            comp1, rel1 = Assembly.abs_to_rel(bindsite1)
            comp2, rel2 = Assembly.abs_to_rel(bindsite2)
            G.add_edge(comp1, comp2, bindsites={comp1: rel1, comp2: rel2})
        return G

    @staticmethod
    def rel_to_abs(
            component_id: str, relative_node_name: str) -> str:
        return f'{component_id}.{relative_node_name}'

    @staticmethod
    def abs_to_rel(
                abs_node_name: str) -> tuple[str, str]:
            comp_id, local_id = abs_node_name.split('.')
            return comp_id, local_id

    @staticmethod
    def bond_to_rough_bond(bond: frozenset[str]) -> frozenset[str]:
        comp1, rel1 = Assembly.abs_to_rel(next(iter(bond)))
        comp2, rel2 = Assembly.abs_to_rel(next(iter(bond - {next(iter(bond))})))
        return frozenset([comp1, comp2])


def assembly_to_graph(
        assembly: Assembly,
        component_structures: Mapping[str, ComponentStructure],
        ) -> nx.Graph:
    G = nx.Graph()
    for comp_id, comp_kind in assembly.component_id_to_kind.items():
        comp_structure = component_structures[comp_kind]
        add_component_to_graph(G, comp_id, comp_kind, comp_structure)
    for bond in assembly.bonds:
        G.add_edge(*bond)
    return G


def add_component_to_graph(
        g: nx.Graph,
        component_id: str, component_kind: str,
        component_structure: ComponentStructure,
        ) -> None:
    # Add the core node
    core_abs = Assembly.rel_to_abs(component_id, 'core')
    g.add_node(
        core_abs, core_or_bindsite='core', component_kind=component_kind)
    
    # Add the binding sites
    for bindsite in component_structure.binding_sites:
        bindsite_abs = Assembly.rel_to_abs(component_id, bindsite)
        g.add_node(bindsite_abs, core_or_bindsite='bindsite')
        g.add_edge(core_abs, bindsite_abs)
    
    # Add the auxiliary edges
    for aux_edge in component_structure.aux_edges:
        bs1_abs = Assembly.rel_to_abs(component_id, aux_edge.bindsite1)
        bs2_abs = Assembly.rel_to_abs(component_id, aux_edge.bindsite2)
        g.add_edge(bs1_abs, bs2_abs, aux_type=aux_edge.aux_type)
