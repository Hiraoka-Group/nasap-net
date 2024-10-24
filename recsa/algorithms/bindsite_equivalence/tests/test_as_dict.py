import pytest

from recsa import Assembly, AuxEdge, Component
from recsa.algorithms.bindsite_equivalence import compute_bindsite_to_root_maps


def test_bindsite_to_root_for_MX4():
    MX4 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')}
    )
    component_structures = {
        'M': Component('M', {'a', 'b', 'c', 'd'}),
        'X': Component('X', {'a'})
    }
    comp_kind_to_map = compute_bindsite_to_root_maps(
        MX4, component_structures)
    
    assert comp_kind_to_map.keys() == {'M', 'X'}
    assert comp_kind_to_map['M'] == {
        'M1.a': 'M1.a', 'M1.b': 'M1.a', 'M1.c': 'M1.a', 'M1.d': 'M1.a'}
    assert comp_kind_to_map['X'] == {
        'X1.a': 'X1.a', 'X2.a': 'X1.a', 'X3.a': 'X1.a', 'X4.a': 'X1.a'}
    

def test_bindsite_to_root_for_MX4_with_aux_edges():
    MX4 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')}
    )
    component_structures = {
        'M': Component(
            'M', {'a', 'b', 'c', 'd'},
            {AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
             AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis')}),
        'X': Component('X', {'a'})
    }
    comp_kind_to_map = compute_bindsite_to_root_maps(
        MX4, component_structures)
    
    assert comp_kind_to_map.keys() == {'M', 'X'}
    assert comp_kind_to_map['M'] == {
        'M1.a': 'M1.a', 'M1.b': 'M1.a', 'M1.c': 'M1.a', 'M1.d': 'M1.a'}
    assert comp_kind_to_map['X'] == {
        'X1.a': 'X1.a', 'X2.a': 'X1.a', 'X3.a': 'X1.a', 'X4.a': 'X1.a'}
    

def test_bindsite_to_root_for_M2LX4():
    M2LX4 = Assembly(
        {
            'M1': 'M', 'M2': 'M', 'L1': 'L', 
            'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {
            ('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'L1.a'),
            ('M2.a', 'L1.b'), ('M2.b', 'X3.a'), ('M2.c', 'X4.a')})
    component_structures = {
        'M': Component('M', {'a', 'b', 'c'}),
        'L': Component('L', {'a', 'b'}),
        'X': Component('X', {'a'})
    }
    comp_kind_to_map = compute_bindsite_to_root_maps(
        M2LX4, component_structures)
    
    assert comp_kind_to_map.keys() == {'M', 'L', 'X'}
    assert comp_kind_to_map['M'] == {
        'M1.a': 'M1.a', 'M1.b': 'M1.a', 'M1.c': 'M1.c',
        'M2.a': 'M1.c', 'M2.b': 'M1.a', 'M2.c': 'M1.a'}
    assert comp_kind_to_map['L'] == {
        'L1.a': 'L1.a', 'L1.b': 'L1.a'}
    assert comp_kind_to_map['X'] == {
        'X1.a': 'X1.a', 'X2.a': 'X1.a', 'X3.a': 'X1.a', 'X4.a': 'X1.a'}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
