import pytest
from frozendict import frozendict

from nasap_net import Assembly, BindingSite, Bond, Component, Reaction, \
    StoichiometricReaction


@pytest.fixture
def M():
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L():
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X():
    return Component(kind='X', sites=[0])


def test_creation_and_str_repr():
    r = StoichiometricReaction({'A': 2, 'B': 1}, {'C': 3}, 1)
    assert isinstance(r.reactants, frozendict)
    assert isinstance(r.products, frozendict)
    assert r.equation_str == '2A + B -> 3C'
    assert str(r) == '2A + B -> 3C (x1)'
    assert repr(r) == '<StoichiometricReaction (2A + B -> 3C)>'


def test_repr_with_id():
    r = StoichiometricReaction({'A': 1}, {'B': 1}, 1, id_='R1')
    assert repr(r) == '<StoichiometricReaction ID=R1 (A -> B)>'


def test_equation_str_coefficients():
    r = StoichiometricReaction({'A': 1, 'B': 2}, {'C': 1}, 1)
    assert r.equation_str == 'A + 2B -> C'


def test_empty_reactants_products():
    r = StoichiometricReaction({}, {}, 1)
    assert r.equation_str == ' -> '


@pytest.mark.parametrize('dup', [0, -1])
def test_invalid_duplicate_count(dup):
    with pytest.raises(ValueError):
        StoichiometricReaction({'A': 1}, {'B': 1}, dup)


def test_immutability():
    r = StoichiometricReaction({'A': 1}, {'B': 1}, 1)
    with pytest.raises(TypeError):
        r.reactants['A'] = 5  # type: ignore
    with pytest.raises(TypeError):
        r.products['B'] = 5  # type: ignore


def test_mapping_types():
    r1 = StoichiometricReaction({'A': 1}, {'B': 1}, 1)
    r2 = StoichiometricReaction(frozendict({'A': 1}), frozendict({'B': 1}), 1)
    assert r1.reactants == r2.reactants
    assert r1.products == r2.products


def test_from_reaction(M, L, X):
    MX2 = Assembly(
        id_='MX2',
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)],
    )
    free_L = Assembly(id_='free_L', components={'L0': L}, bonds=[])
    MLX = Assembly(
        id_='MLX',
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)],
    )
    free_X = Assembly(id_='free_X', components={'X0': X}, bonds=[])

    MX2_plus_free_L = Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4,
    )

    sr = StoichiometricReaction.from_reaction(MX2_plus_free_L)
    assert sr.reactants == frozendict({'MX2': 1, 'free_L': 1})
    assert sr.products == frozendict({'MLX': 1, 'free_X': 1})
    assert sr.duplicate_count == 4


def test_from_reaction_of_same_reactants(M, L, X):
    # MLX + MLX → M2L2X + X
    MLX = Assembly(
        id_='MLX',
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)],
    )
    M2L2X = Assembly(
        id_='M2L2X',
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0), Bond('M1', 1, 'L1', 0),
        ],
    )
    free_X = Assembly(id_='free_X', components={'X0': X}, bonds=[])
    reaction = Reaction(
        init_assem=MLX,
        entering_assem=MLX,
        product_assem=M2L2X,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 1),
        duplicate_count=2,
    )
    sr = StoichiometricReaction.from_reaction(reaction)
    assert sr.reactants == frozendict({'MLX': 2})
    assert sr.products == frozendict({'M2L2X': 1, 'free_X': 1})
    assert sr.duplicate_count == 2


def test_from_reaction_of_same_products(M, L, X):
    MLX = Assembly(
        id_='MLX',
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0)],
    )
    M2L2X = Assembly(
        id_='M2L2X',
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0), Bond('M1', 1, 'L1', 0),
        ],
    )
    free_X = Assembly(id_='free_X', components={'X0': X}, bonds=[])
    reaction = Reaction(
        init_assem=M2L2X,
        entering_assem=free_X,
        product_assem=MLX,
        leaving_assem=MLX,
        metal_bs=BindingSite('M1', 0),
        leaving_bs=BindingSite('L0', 1),
        entering_bs=BindingSite('X0', 0),
        duplicate_count=1,
    )
    sr = StoichiometricReaction.from_reaction(reaction)
    assert sr.reactants == frozendict({'M2L2X': 1, 'free_X': 1})
    assert sr.products == frozendict({'MLX': 2})
    assert sr.duplicate_count == 1


def test_from_reaction_of_intra(M, L, X):
    M2L2X = Assembly(
        id_='M2L2X',
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0), Bond('M1', 1, 'L1', 0),
        ],
    )
    M2L2_ring = Assembly(
        id_='M2L2_ring',
        components={'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('M0', 1, 'L0', 0), Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0), Bond('L1', 1, 'M0', 0),
        ],
    )
    free_X = Assembly(id_='free_X', components={'X0': X}, bonds=[])
    reaction = Reaction(
        init_assem=M2L2X,
        entering_assem=None,
        product_assem=M2L2_ring,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L1', 1),
        duplicate_count=1,
    )
    sr = StoichiometricReaction.from_reaction(reaction)
    assert sr.reactants == frozendict({'M2L2X': 1})
    assert sr.products == frozendict({'M2L2_ring': 1, 'free_X': 1})
    assert sr.duplicate_count == 1


def test_from_reaction_rev_of_intra(M, L, X):
    M2L2X = Assembly(
        id_='M2L2X',
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0), Bond('M1', 1, 'L1', 0),
        ],
    )
    M2L2_ring = Assembly(
        id_='M2L2_ring',
        components={'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('M0', 1, 'L0', 0), Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0), Bond('L1', 1, 'M0', 0),
        ],
    )
    free_X = Assembly(id_='free_X', components={'X0': X}, bonds=[])
    reaction = Reaction(
        init_assem=M2L2_ring,
        entering_assem=free_X,
        product_assem=M2L2X,
        leaving_assem=None,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('L1', 0),
        entering_bs=BindingSite('X0', 0),
        duplicate_count=1,
    )
    sr = StoichiometricReaction.from_reaction(reaction)
    assert sr.reactants == frozendict({'M2L2_ring': 1, 'free_X': 1})
    assert sr.products == frozendict({'M2L2X': 1})
    assert sr.duplicate_count == 1
