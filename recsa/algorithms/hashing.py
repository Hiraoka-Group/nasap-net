from collections.abc import Mapping

import networkx as nx

from recsa import Assembly, ComponentStructure
from recsa.algorithms.aux_edge_existence import has_aux_edges

__all__ = [
    'calc_wl_hash_of_assembly',
    'calc_rough_wl_hash',
    'calc_pure_wl_hash',
    # 'calc_wl_hash_of_graph',
]


def calc_wl_hash_of_assembly(
        assembly: Assembly, 
        component_structures: Mapping[str, ComponentStructure]
        ) -> str:
    if has_aux_edges(assembly, component_structures):
        return calc_pure_wl_hash(assembly, component_structures)
    else:
        return calc_rough_wl_hash(assembly)


def calc_rough_wl_hash(assembly: Assembly) -> str:
    return nx.weisfeiler_lehman_graph_hash(
        assembly.rough_g_snapshot, node_attr='component_kind')


def calc_pure_wl_hash(
        assembly: Assembly, 
        component_structures: Mapping[str, ComponentStructure]
        ) -> str:
    g = assembly.g_snapshot(component_structures)
    _add_attr_for_hash(g)
    
    return nx.weisfeiler_lehman_graph_hash(
        g, node_attr='for_hash', edge_attr='for_hash')


# def calc_wl_hash_of_graph(g: nx.Graph) -> str:
#     g_copy = g.copy()
#     _add_attr_for_hash(g_copy)
    
#     return nx.weisfeiler_lehman_graph_hash(
#         g_copy, node_attr='for_hash', edge_attr='for_hash')


def _add_attr_for_hash(g: nx.Graph) -> None:
    for node, data in g.nodes(data=True):
        if data['core_or_bindsite'] == 'core':
            data['for_hash'] = data['component_kind']
        else:
            data['for_hash'] = None

    for u, v, data in g.edges(data=True):
        if 'aux_kind' in data:
            data['for_hash'] = data['aux_kind']
        else:
            data['for_hash'] = None
