import pytest

from recsa import Assembly, Component, LocalAuxEdge
from recsa.algorithms.bindsite_equivalence import \
    compute_bindsite_equivalence_as_uf
from recsa.algorithms.bindsite_equivalence.as_uf import \
    _update_bindsite_equivalence
from recsa.utils import uf_to_set_of_frozenset


def test__update_bindsite_equivalence():
    pass


def test_uf_for_MX4():
    MX4 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')}
    )
    component_structures = {
        'M': Component('M', {'a', 'b', 'c', 'd'}),
        'X': Component('X', {'a'})
    }
    comp_kind_to_uf = compute_bindsite_equivalence_as_uf(MX4, component_structures)
    assert comp_kind_to_uf.keys() == {'M', 'X'}
    assert uf_to_set_of_frozenset(comp_kind_to_uf['M']) == {
        frozenset({'M1.a', 'M1.b', 'M1.c', 'M1.d'}),
        }
    assert uf_to_set_of_frozenset(comp_kind_to_uf['X']) == {
        frozenset({'X1.a', 'X2.a', 'X3.a', 'X4.a'}),
        }


def test_uf_for_MX4_with_aux_edges():
    MX4 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')}
    )
    component_structures = {
        'M': Component(
            'M', {'a', 'b', 'c', 'd'},
            {LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('b', 'c', 'cis'),
             LocalAuxEdge('c', 'd', 'cis'), LocalAuxEdge('d', 'a', 'cis')}),
        'X': Component('X', {'a'})
    }
    comp_kind_to_uf = compute_bindsite_equivalence_as_uf(MX4, component_structures)

    assert comp_kind_to_uf.keys() == {'M', 'X'}
    assert uf_to_set_of_frozenset(comp_kind_to_uf['M']) == {
        frozenset({'M1.a', 'M1.b', 'M1.c', 'M1.d'}),
        }
    assert uf_to_set_of_frozenset(comp_kind_to_uf['X']) == {
        frozenset({'X1.a', 'X2.a', 'X3.a', 'X4.a'}),
        }


def test_uf_for_M2LX2():
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
    M_COMP = Component('M', {'a', 'b', 'c'})
    L_COMP = Component('L', {'a', 'b'})
    X_COMP = Component('X', {'a'})
    component_structures = {'M': M_COMP, 'L': L_COMP, 'X': X_COMP}
    comp_kind_to_uf = compute_bindsite_equivalence_as_uf(M2LX4, component_structures)

    assert comp_kind_to_uf.keys() == {'M', 'L', 'X'}
    assert uf_to_set_of_frozenset(comp_kind_to_uf['M']) == {
        frozenset({'M1.a', 'M1.b', 'M2.b', 'M2.c'}),
        frozenset({'M1.c', 'M2.a'}),
        }
    assert uf_to_set_of_frozenset(comp_kind_to_uf['L']) == {
        frozenset({'L1.a', 'L1.b'}),
        }
    assert uf_to_set_of_frozenset(comp_kind_to_uf['X']) == {
        frozenset({'X1.a', 'X2.a', 'X3.a', 'X4.a'}),
    }


def test_ML3X():
    ML3X = Assembly(
        {'M1': 'M', 'L1': 'L', 'L2': 'L', 'L3': 'L', 'X1': 'X'},
        {('M1.a', 'L1.a'), ('M1.b', 'L2.a'), ('M1.c', 'L3.a'), ('M1.d', 'X1.a')}
    )
    COMPONENT_STRUCTURES = {
        'M': Component(
            'M', {'a', 'b', 'c', 'd'},
            {LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('b', 'c', 'cis'),
             LocalAuxEdge('c', 'd', 'cis'), LocalAuxEdge('d', 'a', 'cis')}),
        'L': Component('L', {'a', 'b'}),
        'X': Component('X', {'a'})}
    
    comp_kind_to_uf = compute_bindsite_equivalence_as_uf(ML3X, COMPONENT_STRUCTURES)

    assert comp_kind_to_uf.keys() == {'M', 'L', 'X'}
    assert uf_to_set_of_frozenset(comp_kind_to_uf['M']) == {
        frozenset({'M1.a', 'M1.c'}), frozenset({'M1.b'}), frozenset({'M1.d'})}
    assert uf_to_set_of_frozenset(comp_kind_to_uf['L']) == {
        frozenset({'L1.a', 'L3.a'}), frozenset({'L2.a'}),
        frozenset({'L1.b', 'L3.b'}), frozenset({'L2.b'})}
    assert uf_to_set_of_frozenset(comp_kind_to_uf['X']) == {
        frozenset({'X1.a'})}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
