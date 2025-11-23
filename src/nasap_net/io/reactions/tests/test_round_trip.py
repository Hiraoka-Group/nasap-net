import pytest

from nasap_net.io import load_reactions, save_reactions
from nasap_net.models import Assembly, BindingSite, Bond, Component, Reaction


@pytest.fixture
def M():
    return Component(kind='M', sites=[0, 1])

@pytest.fixture
def L():
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X():
    return Component(kind='X', sites=[0])

@pytest.fixture
def MX2(M, X):
    return Assembly(
        id_='MX2',
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )

@pytest.fixture
def free_L(L):
    return Assembly(id_='free_L', components={'L0': L}, bonds=[])

@pytest.fixture
def MLX(M, L, X):
    return Assembly(
        id_='MLX',
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[],
    )

@pytest.fixture
def free_X(X):
    return Assembly(id_='free_X', components={'X0': X}, bonds=[])

@pytest.fixture
def MX2_and_free_L(M, L, X, MX2, free_L, MLX, free_X):
    return Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
        duplicate_count=4,
        id_='R1',
    )


def test_basic(tmp_path, MX2_and_free_L, MX2, free_L, MLX, free_X):
    output_file = tmp_path / 'reactions.csv'
    save_reactions([MX2_and_free_L], output_file)

    loaded_reactions = load_reactions(
        output_file,
        assemblies=[MX2, free_L, MLX, free_X],
        site_id_type='int'
    )

    assert len(loaded_reactions) == 1
    assert loaded_reactions[0] == MX2_and_free_L


def test_nan_handling(tmp_path):
    """Check if NaN values are handled correctly.

    - no entering_assem
    - no leaving_assem
    - no reaction ID
    """
    reaction_with_nan = Reaction(
        init_assem=Assembly(id_='A1', components={}, bonds=[]),
        entering_assem=None,
        product_assem=Assembly(id_='A2', components={}, bonds=[]),
        leaving_assem=None,
        metal_bs=BindingSite('M0', '0'),
        leaving_bs=BindingSite('X0', '0'),
        entering_bs=BindingSite('L0', '0'),
        duplicate_count=1,
        id_=None,
    )

    output_file = tmp_path / 'reactions.csv'
    save_reactions([reaction_with_nan], output_file)

    loaded_reactions = load_reactions(
        output_file,
        assemblies=[
            Assembly(id_='A1', components={}, bonds=[]),
            Assembly(id_='A2', components={}, bonds=[]),
        ],
    )

    assert len(loaded_reactions) == 1
    assert loaded_reactions[0] == reaction_with_nan
