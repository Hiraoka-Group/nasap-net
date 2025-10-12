from nasap_net.reaction_exploration_im.lib.igraph import get_isomorphism, \
    is_isomorphic
from nasap_net.reaction_exploration_im.models import Assembly, BindingSite, \
    Bond, Component


def test_is_isomorphic():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MLX = Assembly(
        components={'M1': M, 'L1': L, 'X1': X},
        bonds=[Bond('M1', 'L1', 0, 0), Bond('M1', 'X1', 1, 0)]
    )
    MLX_permuted = Assembly(
        components={'L1': L, 'X1': X, 'M1': M},
        bonds=[Bond('M1', 'X1', 1, 0), Bond('M1', 'L1', 0, 0)]
    )
    assert is_isomorphic(MLX, MLX_permuted)


def test_get_isomorphism():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MLX = Assembly(
        components={'M1': M, 'L1': L, 'X1': X},
        bonds=[Bond('M1', 'L1', 0, 0), Bond('M1', 'X1', 1, 0)]
    )
    MLX_permuted = Assembly(
        components={'L2': L, 'X2': X, 'M2': M},
        bonds=[Bond('M2', 'L2', 1, 0), Bond('M2', 'X2', 0, 0)]
    )
    isom = get_isomorphism(MLX, MLX_permuted)
    assert isom.comp_id_mapping == {'M1': 'M2', 'L1': 'L2', 'X1': 'X2'}
    assert isom.binding_site_mapping == {
        BindingSite('M1', 0): BindingSite('M2', 1),
        BindingSite('M1', 1): BindingSite('M2', 0),
        BindingSite('L1', 0): BindingSite('L2', 0),
        BindingSite('L1', 1): BindingSite('L2', 1),
        BindingSite('X1', 0): BindingSite('X2', 0),
    }
