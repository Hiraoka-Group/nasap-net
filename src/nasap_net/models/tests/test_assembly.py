import pytest

from nasap_net.models import Assembly, Bond, Component
from nasap_net.models.exceptions import InconsistentComponentKindError


def test_assembly():
    L = Component(kind='L', sites=[0, 1])
    M = Component(kind='M', sites=[0, 1])
    assembly = Assembly(
        components={'L1': L, 'M1': M},
        bonds={Bond('L1', 0, 'M1', 0)},
        )
    assert assembly.components == {'L1': L, 'M1': M}
    assert assembly.bonds == frozenset({Bond('L1', 0, 'M1', 0)})


def test_inconsistent_component_kind_error():
    L1 = Component(kind='L', sites=[0, 1])
    L2 = Component(kind='L', sites=[2, 3])
    with pytest.raises(InconsistentComponentKindError):
        Assembly(
            components={'L0': L1, 'L1': L2},
            bonds=set()
        )
