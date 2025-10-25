import pytest

from nasap_net.models import AuxEdge, Component
from nasap_net.yaml.lib import dump_components, load_components


@pytest.fixture
def components():
    return {
        'M_square': Component(
            kind='M_square', sites=[0, 1, 2, 3],
            aux_edges=[
                AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)
            ]
        ),
        'X': Component(kind='X', sites=[0]),
    }

@pytest.fixture
def dumped_components():
    return """M_square: !Component
  kind: M_square
  sites: [0, 1, 2, 3]
  aux_edges:
  - sites: [0, 1]
  - sites: [0, 3]
  - sites: [1, 2]
  - sites: [2, 3]
X: !Component
  kind: X
  sites: [0]
"""


def test_dump_components(components, dumped_components):
    dumped = dump_components(components)
    assert dumped == dumped_components


def test_load_components(components, dumped_components):
    loaded = load_components(dumped_components)
    assert loaded == components


def test_round_trip():
    components = {
        'M': Component(kind='M', sites=[0, 1]),
        'M_square': Component(
            kind='M', sites=[0, 1, 2, 3],
            aux_edges=[
                AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)
            ]
        ),
        'X': Component(kind='X', sites=[0]),
        'L': Component(kind='L', sites=[0, 1]),
    }
    dumped = dump_components(components)
    loaded = load_components(dumped)
    assert loaded == components
