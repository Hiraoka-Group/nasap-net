from frozendict import frozendict

from nasap_net.isomorphism import Isomorphism, \
    get_all_isomorphisms, \
    get_isomorphism, \
    is_isomorphic
from nasap_net.models import Assembly, BindingSite, Bond, Component


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


def test_get_all_isomorphisms():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MX2 = Assembly(
        components={'M1': M, 'X1': X, 'X2': X},
        bonds=[Bond('M1', 'X1', 0, 0), Bond('M1', 'X2', 1, 0)]
    )
    MX2_2 = Assembly(
        components={'M10': M, 'X10': X, 'X20': X},
        bonds=[Bond('M10', 'X10', 0, 0), Bond('M10', 'X20', 1, 0)]
    )

    isoms = get_all_isomorphisms(MX2, MX2_2)
    assert len(isoms) == 2
    assert isoms == {
        Isomorphism(
            comp_id_mapping=frozendict(
                {'M1': 'M10', 'X1': 'X10', 'X2': 'X20'}),
            binding_site_mapping=frozendict({
                BindingSite('M1', 0): BindingSite('M10', 0),
                BindingSite('M1', 1): BindingSite('M10', 1),
                BindingSite('X1', 0): BindingSite('X10', 0),
                BindingSite('X2', 0): BindingSite('X20', 0),
            })
        ),
        Isomorphism(
            comp_id_mapping=frozendict(
                {'M1': 'M10', 'X1': 'X20', 'X2': 'X10'}),
            binding_site_mapping=frozendict({
                BindingSite('M1', 0): BindingSite('M10', 1),
                BindingSite('M1', 1): BindingSite('M10', 0),
                BindingSite('X1', 0): BindingSite('X20', 0),
                BindingSite('X2', 0): BindingSite('X10', 0),
            })
        ),
    }
