import pytest

from nasap_net import Assembly, BindingSite, Bond, Component, Reaction
from nasap_net.reaction_pairing import is_forward_reverse_equivalent


@pytest.fixture
def M() -> Component:
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L() -> Component:
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X() -> Component:
    return Component(kind='X', sites=[0])


def test_same_type_substitution_is_equivalent(M, X):
    """True when forward and reverse are structurally identical. (MX2 + X -> MX2 + X)"""
    init_MX2 = Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
    )
    entering_X = Assembly(components={'X2': X}, bonds=[])
    product_MX2 = Assembly(
        components={'M0': M, 'X2': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X2', 0), Bond('M0', 1, 'X1', 0)]
    )
    leaving_X = Assembly(components={'X0': X}, bonds=[])

    reaction = Reaction(
        init_assem=init_MX2,
        entering_assem=entering_X,
        product_assem=product_MX2,
        leaving_assem=leaving_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('X2', 0),
    )

    assert is_forward_reverse_equivalent(reaction)


def test_different_type_substitution_is_not_equivalent(M, L, X):
    """False when forward and reverse differ structurally. (MX2 + L -> MLX + X)"""
    MX2 = Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_L = Assembly(components={'L0': L}, bonds=[])
    MLX = Assembly(
        components={'M0': M, 'L0': L, 'X1': X},
        bonds=[Bond('M0', 0, 'L0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_X = Assembly(components={'X0': X}, bonds=[])

    reaction = Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
    )

    assert not is_forward_reverse_equivalent(reaction)
