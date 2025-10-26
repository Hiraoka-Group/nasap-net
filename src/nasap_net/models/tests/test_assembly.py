import pytest

from nasap_net.models import Assembly, Bond, Component
from nasap_net.models.assembly import InconsistentComponentError


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
    with pytest.raises(InconsistentComponentError):
        Assembly(
            components={'L0': L1, 'L1': L2},
            bonds=set()
        )


def test___repr__():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    assembly = Assembly(
        components={'X0': X, 'M0': M, 'X1': X},
        bonds={Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)},
    )
    expected_repr = (
        "<Assembly components={'M0': 'M', 'X0': 'X', 'X1': 'X'}, "
        "bonds=[('M0', 0, 'X0', 0), ('M0', 1, 'X1', 0)]>"
    )
    assert repr(assembly) == expected_repr


def test___repr___with_id():
    X = Component(kind='X', sites=[0])
    assembly = Assembly(
        id_='free_X',
        components={'X0': X},
        bonds=[],
    )
    expected_repr = (
        "<Assembly id='free_X', components={'X0': 'X'}, bonds=[]>"
    )
    assert repr(assembly) == expected_repr


def test___repr___with_no_bonds():
    X = Component(kind='X', sites=[0])
    assembly = Assembly(
        components={'X0': X},
        bonds=[],
    )
    expected_repr = (
        "<Assembly components={'X0': 'X'}, bonds=[]>"
    )
    assert repr(assembly) == expected_repr
