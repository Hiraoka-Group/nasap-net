import yaml

from nasap_net.models import AuxEdge, Component


class ComponentLoader(yaml.SafeLoader):
    def ignore_aliases(self, data):
        return True


def _component_constructor(loader: yaml.Loader, node: yaml.Node) -> Component:
    assert isinstance(node, yaml.MappingNode)
    mapping = loader.construct_mapping(node, deep=True)
    kind = mapping['kind']
    sites = mapping['sites']
    aux_edges = [
        AuxEdge(*m['sites'], kind=m.get('kind'))
        for m in mapping.get('aux_edges', [])]
    return Component(kind=kind, sites=sites, aux_edges=aux_edges)


yaml.add_constructor('!Component', _component_constructor, Loader=ComponentLoader)
