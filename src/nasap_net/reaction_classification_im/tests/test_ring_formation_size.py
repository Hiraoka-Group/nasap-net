import pytest

from nasap_net.models import Assembly, BindingSite, Bond, Component, Reaction
from nasap_net.reaction_classification_im import get_min_forming_ring_size


@pytest.fixture
def M() -> Component:
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L() -> Component:
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X() -> Component:
    return Component(kind='X', sites=[0])


def test_basic(M, L, X):
    # X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
    M2L2X = Assembly(
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0),
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
        ],
    )
    # //-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)-//
    M2L2_ring = Assembly(
        components={'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
            Bond('L1', 1, 'M0', 0),
        ],
    )
    free_X = Assembly(components={'X0': X}, bonds=[])

    reaction = Reaction(
        init_assem=M2L2X,
        entering_assem=None,
        product_assem=M2L2_ring,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L1', 1),
    )
    assert get_min_forming_ring_size(reaction) == 4


def test_no_ring(M, L, X):
    # X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
    M2L2X = Assembly(
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0),
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
        ],
    )
    # X0(0)-(0)M0(1)-(1)L1(0)-(1)M1(0)-(1)L0(0)
    M2L2X_after = Assembly(
        components={'X0': X, 'M0': M, 'L1': L, 'M1': M, 'L0': L},
        bonds=[
            Bond('X0', 0, 'M0', 0),
            Bond('M0', 1, 'L1', 1),
            Bond('L1', 0, 'M1', 1),
            Bond('M1', 0, 'L0', 1),
        ],
    )
    reaction = Reaction(
        init_assem=M2L2X,
        entering_assem=None,
        product_assem=M2L2X_after,
        leaving_assem=None,
        metal_bs=BindingSite('M0', 1),
        leaving_bs=BindingSite('L0', 0),
        entering_bs=BindingSite('L1', 1),
    )
    assert get_min_forming_ring_size(reaction) is None


def test_inter_reaction(M, L, X):
    MX2 = Assembly(
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_L = Assembly(components={'L0': L}, bonds=[])
    MLX = Assembly(
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)]
    )
    free_X = Assembly(components={'X1': X}, bonds=[])

    reaction = Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
    )

    assert get_min_forming_ring_size(reaction) is None
