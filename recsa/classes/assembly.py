from __future__ import annotations

from collections.abc import Iterable, Iterator, Mapping
from copy import deepcopy
from dataclasses import dataclass
from itertools import chain
from types import MappingProxyType
from typing import Literal, overload

import networkx as nx
from frozendict import frozendict

from recsa import RecsaValueError

from .bindsite_id_converter import BindsiteIdConverter
from .component import Component

__all__ = ['Assembly', 'assembly_to_graph', 'assembly_to_rough_graph', 'find_free_bindsites']


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
        if component_id_to_kind is None:
            self.__components = frozendict[str, str]()
        else:
            self.__components = frozendict(component_id_to_kind)
        self.__bonds = frozenset(
            frozenset(bond) for bond in (bonds or []))

        self._graph_cache = None
        self._rough_graph_cache = None

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
    def bonds(self) -> frozenset[frozenset[str]]:
        return self.__bonds
    
    @property
    def bindsite_to_connected(self) -> dict[str, str]:
        """Return a dictionary of the connected binding sites.
        
        Only the binding sites that are connected to other binding sites
        are included in the returned object.
        """
        bindsite_to_connected = {}
        for bindsite1, bindsite2 in self.__bonds:
            bindsite_to_connected[bindsite1] = bindsite2
            bindsite_to_connected[bindsite2] = bindsite1
        return bindsite_to_connected
    
    def g_snapshot(
            self, component_structures: Mapping[str, Component]
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

    def with_added_component(
            self, component_id: str, component_kind: str) -> Assembly:
        return Assembly(
            self.component_id_to_kind | {component_id: component_kind},
            self.bonds)
    
    def with_added_components(
            self, components: Iterable[tuple[str, str]]) -> Assembly:
        return Assembly(
            self.component_id_to_kind | dict(components),
            self.bonds)
    
    def with_added_bond(
            self, bindsite1: str, bindsite2: str) -> Assembly:
        # TODO: Should raise Error if the bond already exists.
        id_converter = BindsiteIdConverter()
        comp1, rel1 = id_converter.global_to_local(bindsite1)
        comp2, rel2 = id_converter.global_to_local(bindsite2)
        for comp in [comp1, comp2]:
            if comp not in self.__components:
                raise RecsaValueError(
                    f'The component "{comp}" does not exist in the assembly.')
        return Assembly(
            self.component_id_to_kind,
            self.bonds | {frozenset([bindsite1, bindsite2])})
    
    def with_added_bonds(
            self, bonds: Iterable[tuple[str, str]]) -> Assembly:
        id_converter = BindsiteIdConverter()
        for bindsite1, bindsite2 in bonds:
            comp1, rel1 = id_converter.global_to_local(bindsite1)
            comp2, rel2 = id_converter.global_to_local(bindsite2)
            for comp in [comp1, comp2]:
                if comp not in self.__components:
                    raise RecsaValueError(
                        f'The component "{comp}" does not exist in the assembly.')
        return Assembly(
            self.component_id_to_kind,
            self.bonds | {frozenset([bindsite1, bindsite2]) for bindsite1, bindsite2 in bonds})

    def with_removed_bond(
            self, bindsite1: str, bindsite2: str) -> Assembly:
        return Assembly(
            self.component_id_to_kind,
            self.bonds - {frozenset([bindsite1, bindsite2])})

    def with_removed_bonds(
            self, bonds: Iterable[tuple[str, str]]) -> Assembly:
        return Assembly(
            self.component_id_to_kind,
            self.bonds - {frozenset([bindsite1, bindsite2]) for bindsite1, bindsite2 in bonds})
    
    # ============================================================
    # Methods to relabel the assembly
    # ============================================================
    
    def rename_component_ids(
            self, mapping: Mapping[str, str]) -> Assembly:
        assem = deepcopy(self)

        id_converter = BindsiteIdConverter()

        new_components = {}
        for old_id, component in assem.__components.items():
            new_id = mapping.get(old_id, old_id)
            new_components[new_id] = component
        
        new_bonds = set()
        for bindsite1, bindsite2 in assem.__bonds:
            comp1, rel1 = id_converter.global_to_local(bindsite1)
            comp2, rel2 = id_converter.global_to_local(bindsite2)
            new_bindsite1 = id_converter.local_to_global(
                mapping.get(comp1, comp1), rel1)
            new_bindsite2 = id_converter.local_to_global(
                mapping.get(comp2, comp2), rel2)
            new_bonds.add(frozenset([new_bindsite1, new_bindsite2]))

        assem.__components = frozendict(new_components)
        assem.__bonds = frozenset(new_bonds)
        assem._rough_graph_cache = None

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
        connected = self.bindsite_to_connected.get(bindsite)
        if connected is None and error_if_free:
            raise RecsaValueError(
                f'The binding site "{bindsite}" is free.')
        return connected
    
    def is_free_bindsite(self, bindsite: str) -> bool:
        return self.get_connected_bindsite(bindsite) is None
    
    def get_component_kind(self, component_id: str) -> str:
        return self.__components[component_id]
    
    def get_component_kind_of_core(self, core: str) -> str:
        id_converter = BindsiteIdConverter()
        comp_id, rel = id_converter.global_to_local(core)
        return self.get_component_kind(comp_id)
    
    def get_component_kind_of_bindsite(self, bindsite: str) -> str:
        id_converter = BindsiteIdConverter()
        comp_id, rel = id_converter.global_to_local(bindsite)
        return self.get_component_kind(comp_id)
    
    def deepcopy(self) -> Assembly:
        return deepcopy(self)
    
    def get_core_of_the_component(self, component_id: str) -> str:
        id_converter = BindsiteIdConverter()
        return id_converter.local_to_global(component_id, 'core')

    def iter_all_cores(self) -> Iterator[str]:
        id_converter = BindsiteIdConverter()
        for comp_id, comp_kind in self.component_id_to_kind.items():
            yield id_converter.local_to_global(comp_id, 'core')
    
    def get_all_bindsites(
            self, component_structures: Mapping[str, Component]
            ) -> set[str]:
        """Get all the binding sites in the assembly."""
        # TODO: Consider yielding the binding sites instead of returning a set.
        id_converter = BindsiteIdConverter()
        all_bindsites = set()
        for comp_id, comp_kind in self.component_id_to_kind.items():
            comp_struct = component_structures[comp_kind]
            for bindsite in comp_struct.bindsites:
                all_bindsites.add(id_converter.local_to_global(comp_id, bindsite))
        return all_bindsites

    def iter_aux_edges(
            self, component_structures: Mapping[str, Component]
            ) -> Iterator[AbsAuxEdge]:
        id_converter = BindsiteIdConverter()
        for comp_id, comp_kind in self.component_id_to_kind.items():
            comp_struct = component_structures[comp_kind]
            for rel_aux_edge in comp_struct.aux_edges:
                yield AbsAuxEdge(
                    id_converter.local_to_global(
                        comp_id, rel_aux_edge.local_bindsite1),
                    id_converter.local_to_global(
                        comp_id, rel_aux_edge.local_bindsite2),
                    rel_aux_edge.aux_kind)

    def get_bindsites_of_component(
            self, component_id: str, 
            component_structures: Mapping[str, Component]
            ) -> set[str]:
        """Get the binding sites of the component."""
        id_converter = BindsiteIdConverter()
        comp_kind = self.get_component_kind(component_id)
        comp_struct = component_structures[comp_kind]
        return {
            id_converter.local_to_global(component_id, bindsite)
            for bindsite in comp_struct.bindsites}
    
    def get_all_bindsites_of_kind(
            self, component_kind: str,
            component_structures: Mapping[str, Component],
            ) -> Iterator[str]:
        for comp_id, comp in self.component_id_to_kind.items():
            if comp == component_kind:
                yield from self.get_bindsites_of_component(
                    comp_id, component_structures)

    def find_free_bindsites(
            self, component_structures: Mapping[str, Component]
            ) -> set[str]:
        """Find free bindsites."""
        id_converter = BindsiteIdConverter()
        all_bindsites = {
            id_converter.local_to_global(comp_id, bindsite)
            for comp_id, comp_kind in self.component_id_to_kind.items()
            for bindsite in component_structures[comp_kind].bindsites
        }
        connected_bindsites = chain(*self.bonds)
        free_bindsites = all_bindsites - set(connected_bindsites)
        return free_bindsites

    # ============================================================
    # Methods to convert the assembly to graphs
    # ============================================================

    def _to_graph(
            self, component_kinds: Mapping[str, Component]
            ) -> nx.Graph:
        return assembly_to_graph(self, component_kinds)

    def _to_rough_graph(self) -> nx.Graph:
        id_converter = BindsiteIdConverter()
        G = nx.Graph()
        for comp_id, comp_kind in self.component_id_to_kind.items():
            G.add_node(comp_id, component_kind=comp_kind)
        for bindsite1, bindsite2 in self.bonds:
            comp1, rel1 = id_converter.global_to_local(bindsite1)
            comp2, rel2 = id_converter.global_to_local(bindsite2)
            G.add_edge(comp1, comp2, bindsites={comp1: rel1, comp2: rel2})
        return G

    @classmethod
    def bond_to_rough_bond(
            cls, bond: frozenset[str]) -> frozenset[str]:
        id_converter = BindsiteIdConverter()
        comp1, rel1 = id_converter.global_to_local(next(iter(bond)))
        comp2, rel2 = id_converter.global_to_local(next(iter(bond - {next(iter(bond))})))
        return frozenset([comp1, comp2])


def assembly_to_graph(
        assembly: Assembly,
        component_structures: Mapping[str, Component],
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
        component_structure: Component,
        ) -> None:
    # Add the core node
    id_converter = BindsiteIdConverter()
    core_abs = id_converter.local_to_global(component_id, 'core')
    g.add_node(
        core_abs, core_or_bindsite='core', component_kind=component_kind)
    
    # Add the binding sites
    for bindsite in component_structure.bindsites:
        bindsite_abs = id_converter.local_to_global(component_id, bindsite)
        g.add_node(bindsite_abs, core_or_bindsite='bindsite')
        g.add_edge(core_abs, bindsite_abs)
    
    # Add the auxiliary edges
    for aux_edge in component_structure.aux_edges:
        bs1_abs = id_converter.local_to_global(component_id, aux_edge.local_bindsite1)
        bs2_abs = id_converter.local_to_global(component_id, aux_edge.local_bindsite2)
        g.add_edge(bs1_abs, bs2_abs, aux_type=aux_edge.aux_kind)
