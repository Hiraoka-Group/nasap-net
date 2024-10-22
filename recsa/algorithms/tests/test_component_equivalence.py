import pytest

from recsa import Assembly, compute_component_equivalence
from recsa.algorithms.component_equivalence import \
    _update_component_equivalence


def test__update_component_equivalence():
    pass


def test_compute_component_equivalence_MX4():
    MX4 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')}
    )
    uf = compute_component_equivalence(MX4)
    assert set(frozenset(group) for group in uf.to_sets()) == {
        frozenset({'M1'}), frozenset({'X1', 'X2', 'X3', 'X4'})
    }


def test_compute_component_equivalence_M2LX4():
    # X1(a)--(a)M1(c)--(a)L1(b)--(a)M2(c)--(a)X4
    #          (b)                 (b)
    #           |                   |
    #          (a)                 (a)
    #           X2                  X3
    M2LX4 = Assembly(
        {
            'M1': 'M', 'M2': 'M', 'L1': 'L', 
            'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {
            ('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'L1.a'),
            ('M2.a', 'L1.b'), ('M2.b', 'X3.a'), ('M2.c', 'X4.a')})
    uf = compute_component_equivalence(M2LX4)
    assert set(frozenset(group) for group in uf.to_sets()) == {
        frozenset({'M1', 'M2'}),
        frozenset({'X1', 'X2', 'X3', 'X4'}),
        frozenset({'L1'})
    }


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
