import pytest

from recsa import Assembly, Component, assemblies_equal, perform_intra_exchange


def test_intra_exchange() -> None:
    COMPONENT_KINDS = {
        'M': Component('M', {'a', 'b'}),
        'L': Component('L', {'a', 'b'}),
        'X': Component('X', {'a'})}
    
    # X1(a)--(a)M1(b)--(a)L1(b)
    MLX = Assembly(
        COMPONENT_KINDS,
        {'M1': 'M', 'X1': 'X', 'L1': 'L'},
        [('X1.a', 'M1.a'), ('M1.b', 'L1.a')])
    # Expected product: ML ring
    ML_RING = Assembly(
        COMPONENT_KINDS,
        {'M1': 'M', 'L1': 'L'},
        [('M1.b', 'L1.a'), ('L1.b', 'M1.a')])
    # Expected leaving: X
    X = Assembly(COMPONENT_KINDS, {'X1': 'X'}, [])

    product, leaving = perform_intra_exchange(
        MLX, 'M1.a', 'X1.a', 'L1.b')

    assert assemblies_equal(product, ML_RING, COMPONENT_KINDS)
    assert leaving is not None
    assert assemblies_equal(leaving, X, COMPONENT_KINDS)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
