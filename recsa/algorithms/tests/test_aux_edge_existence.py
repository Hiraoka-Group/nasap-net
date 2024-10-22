import pytest

from recsa import Assembly, ComponentStructure, LocalAuxEdge, has_aux_edges


def test_has_aux_edges_true():
    MX4 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')])
    COMPONENT_STRUCTURES = {
        'M': ComponentStructure(
            'M', {'a', 'b', 'c', 'd'}, 
            {LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('b', 'c', 'cis'),
             LocalAuxEdge('c', 'd', 'cis'), LocalAuxEdge('d', 'a', 'cis')}),
        'X': ComponentStructure('X', {'a'})}
    assert has_aux_edges(MX4, COMPONENT_STRUCTURES)


def test_has_aux_edges_false():
    MX4 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')])
    COMPONENT_STRUCTURES = {
        'M': ComponentStructure('M', {'a', 'b', 'c', 'd'}),  # No aux edges
        'X': ComponentStructure('X', {'a'})}
    assert not has_aux_edges(MX4, COMPONENT_STRUCTURES)


def test_has_aux_edges_false2():
    MX4 = Assembly(
        {'M1': 'M', 'X1': 'X', 'X2': 'X', 'X3': 'X', 'X4': 'X'},
        [('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'X4.a')])
    COMPONENT_STRUCTURES = {
        'M': ComponentStructure('M', {'a', 'b', 'c', 'd'}),  # No aux edges
        'L': ComponentStructure(
            'L', {'a', 'b', 'c', 'd'},
            {LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('b', 'c', 'cis'),
             LocalAuxEdge('c', 'd', 'cis'), LocalAuxEdge('d', 'a', 'cis')}),  # Aux edges but not in assembly
        'X': ComponentStructure('X', {'a'})}
    assert not has_aux_edges(MX4, COMPONENT_STRUCTURES)



if __name__ == '__main__':
    pytest.main(['-vv', __file__])
