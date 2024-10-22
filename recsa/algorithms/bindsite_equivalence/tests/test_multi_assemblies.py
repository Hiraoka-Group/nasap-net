import pytest

from recsa import (Assembly, AuxEdge, ComponentStructure,
                   compute_bindsite_to_root_maps_for_multi_assemblies)


def test_maps():
    MX4 = Assembly(
        {'M1': 'M_TETRA', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')}
    )
    M2LX4 = Assembly(
        {
            'M1': 'M_TRI', 'M2': 'M_TRI', 'L1': 'L', 
            'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        {
            ('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'L1.a'),
            ('M2.a', 'L1.b'), ('M2.b', 'X3.a'), ('M2.c', 'X4.a')})
    ID_TO_ASSEMBLY = {'MX4': MX4, 'M2LX4': M2LX4}

    COMPONENT_STRUCTURES = {
        'M_TRI': ComponentStructure('M', {'a', 'b', 'c'}),
        'M_TETRA': ComponentStructure(
            'M', {'a', 'b', 'c', 'd'},
            {AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
             AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis')}),
        'L': ComponentStructure('L', {'a', 'b'}), 
        'X': ComponentStructure('X', {'a'})
        }
    
    bindsite_to_root_maps = compute_bindsite_to_root_maps_for_multi_assemblies(
        ID_TO_ASSEMBLY, COMPONENT_STRUCTURES)
    
    assert bindsite_to_root_maps.keys() == {
        ('MX4', 'M_TETRA'), ('MX4', 'X'),
        ('M2LX4', 'M_TRI'), ('M2LX4', 'L'), ('M2LX4', 'X')}
    assert bindsite_to_root_maps[('MX4', 'M_TETRA')] == {
        'M1.a': 'M1.a', 'M1.b': 'M1.a', 'M1.c': 'M1.a', 'M1.d': 'M1.a'}
    assert bindsite_to_root_maps[('MX4', 'X')] == {
        'X1.a': 'X1.a', 'X2.a': 'X1.a', 'X3.a': 'X1.a', 'X4.a': 'X1.a'}
    assert bindsite_to_root_maps[('M2LX4', 'M_TRI')] == {
        'M1.a': 'M1.a', 'M1.b': 'M1.a', 'M1.c': 'M1.c',
        'M2.a': 'M1.c', 'M2.b': 'M1.a', 'M2.c': 'M1.a'}
    assert bindsite_to_root_maps[('M2LX4', 'L')] == {
        'L1.a': 'L1.a', 'L1.b': 'L1.a'}
    assert bindsite_to_root_maps[('M2LX4', 'X')] == {
        'X1.a': 'X1.a', 'X2.a': 'X1.a', 'X3.a': 'X1.a', 'X4.a': 'X1.a'}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
