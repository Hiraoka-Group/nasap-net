import networkx as nx

__all__ = ['add_attr_to_edges']


def add_attr_to_edges(g: nx.Graph):
    for u, v, data in g.edges(data=True):
        if 'aux_type' in data:
            data['edge_type'] = 'aux'
        else:
            core_or_bindsite_u = g.nodes[u]['core_or_bindsite']
            core_or_bindsite_v = g.nodes[v]['core_or_bindsite']
            if core_or_bindsite_u == 'bindsite' and core_or_bindsite_v == 'bindsite':
                data['edge_type'] = 'bindsite_to_bindsite'
            else:
                data['edge_type'] = 'core_to_bindsite'
    return g
