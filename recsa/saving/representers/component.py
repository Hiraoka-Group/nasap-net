import yaml

from recsa import Component

from .aux_edge import add_aux_edge_representer

add_aux_edge_representer()


def component_representer(dumper, data: Component):
    component_dict = {
        'id': data.kind,
        'bindsites': list(data.bindsites),
        'aux_edges': list(data.aux_edges),
    }
    return dumper.represent_dict(component_dict)


def add_component_representer():
    yaml.add_representer(Component, component_representer)
