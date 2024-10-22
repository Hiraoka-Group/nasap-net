import pytest

from recsa import (Assembly, AuxEdge, ComponentStructure, MleBindsite, MleKind,
                   find_mles_by_kind)


def test_find_mles_by_kind() -> None:
    MLX = Assembly(
        {'M1': 'M', 'L1': 'L', 'X1': 'X'},
        {('M1.a', 'L1.a'), ('M1.b', 'X1.a')}
    )
    MLE_KINDS = [
        MleKind(metal='M', entering='L', leaving='X'),
    ]
    COMPONENT_STRUCTURES = {
        'M': ComponentStructure('M', {'a', 'b'}),
        'L': ComponentStructure('L', {'a', 'b'}),
        'X': ComponentStructure('X', {'a'})
    }
    mles = find_mles_by_kind(
        MLX, MleKind(metal='M', entering='L', leaving='X'), 
        COMPONENT_STRUCTURES)
    
    assert set(mles) == {
        MleBindsite('M1.b', 'X1.a', 'L1.b'),
    }


def test_find_mles_by_kind_with_aux_edges() -> None:
    MLX3 = Assembly(
        {'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
        {('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'L1.a')}
    )
    MLE_KINDS = [
        MleKind(metal='M', entering='L', leaving='X'),
    ]
    COMPONENT_STRUCTURES = {
        'M': ComponentStructure(
            'M', {'a', 'b', 'c', 'd'},
            {AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
             AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis')}),
        'L': ComponentStructure('L', {'a', 'b'}),
        'X': ComponentStructure('X', {'a'})
    }
    mles = find_mles_by_kind(
        MLX3, MleKind(metal='M', entering='L', leaving='X'), 
        COMPONENT_STRUCTURES)
    
    assert set(mles) == {
        MleBindsite('M1.b', 'X2.a', 'L1.b'),
        MleBindsite('M1.a', 'X1.a', 'L1.b'),
        MleBindsite('M1.c', 'X3.a', 'L1.b'),
    }


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
