import pytest

from recsa import Assembly, ComponentStructure, LocalAuxEdge, isomorphisms_iter


def test_isomorphisms_iter():
    ML2X2_CIS = Assembly(
        {'M1': 'M', 'L1': 'L', 'L2': 'L', 'X1': 'X', 'X2': 'X'},
        [('M1.a', 'L1.a'), ('M1.b', 'L2.a'), ('M1.c', 'X1.a'), ('M1.d', 'X2.a')])
    COMPONENT_STRUCTURES = {
        'M': ComponentStructure(
            'M', {'a', 'b', 'c', 'd'},
            {LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('b', 'c', 'cis'),
             LocalAuxEdge('c', 'd', 'cis'), LocalAuxEdge('d', 'a', 'cis')}),
        'L': ComponentStructure('L', {'a'}),
        'X': ComponentStructure('X', {'a'})}
    
    isomorphisms = list(isomorphisms_iter(ML2X2_CIS, ML2X2_CIS, COMPONENT_STRUCTURES))

    # TODO: Refactor assertions to use compare_mapping_iterables
    assert len(isomorphisms) == 2
    assert {'M1.core': 'M1.core', 'L1.core': 'L1.core', 'L2.core': 'L2.core',
            'X1.core': 'X1.core', 'X2.core': 'X2.core',
            'M1.a': 'M1.a', 'M1.b': 'M1.b', 'M1.c': 'M1.c', 'M1.d': 'M1.d',
            'L1.a': 'L1.a', 'L2.a': 'L2.a', 'X1.a': 'X1.a', 'X2.a': 'X2.a'} in isomorphisms
    assert {'M1.core': 'M1.core', 'L1.core': 'L2.core', 'L2.core': 'L1.core',
            'X1.core': 'X2.core', 'X2.core': 'X1.core',
            'M1.a': 'M1.b', 'M1.b': 'M1.a', 'M1.c': 'M1.d', 'M1.d': 'M1.c',
            'L1.a': 'L2.a', 'L2.a': 'L1.a', 'X1.a': 'X2.a', 'X2.a': 'X1.a'} in isomorphisms


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
