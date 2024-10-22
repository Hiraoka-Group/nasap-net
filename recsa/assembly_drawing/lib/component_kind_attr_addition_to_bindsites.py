import networkx as nx

__all__ = ['add_component_kind_attr_to_bindsites']


def add_component_kind_attr_to_bindsites(g: nx.Graph):
    """Adds 'component' attribute to 'bindsite' nodes.

    Args:
        g (nx.Graph): A graph representing an assembly.
    """
    for node in g.nodes:
        if g.nodes[node]['core_or_bindsite'] == 'core':
            component = g.nodes[node]['component_kind']
            # Iterate over adj nodes of the core node
            for adj_node in g.adj[node]:
                assert g.nodes[adj_node]['core_or_bindsite'] == 'bindsite'
                g.nodes[adj_node]['component_kind'] = component
