import yaml

from nasap_net.models import AuxEdge, Component
from nasap_net.yaml.separative.lib import ComponentDumper, ComponentLoader


def test_component_dump_and_load():
    M_square = Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])
    # dump
    yaml_str = yaml.dump(M_square, Dumper=ComponentDumper)
    # load
    loaded = yaml.load(yaml_str, Loader=ComponentLoader)
    assert loaded == M_square
