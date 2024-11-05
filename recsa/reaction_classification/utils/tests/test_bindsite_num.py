import pytest

from recsa import Assembly, Component
from recsa.reaction_classification.utils import get_connected_num


def test_free():
    M_COMP = Component(['a', 'b'])
    FREE_M = Assembly({'M1': 'M'})
    assert get_connected_num(FREE_M, 'M1', 'L', M_COMP) == 0


def test_one_connected():
    M_COMP = Component(['a', 'b'])
    ML = Assembly({'M1': 'M', 'L1': 'L'}, [('M1.a', 'L1.a')])
    assert get_connected_num(ML, 'M1', 'L', M_COMP) == 1


def test_two_connected():
    M_COMP = Component(['a', 'b'])
    ML = Assembly({'M1': 'M', 'L1': 'L', 'L2': 'L'},
                   [('M1.a', 'L1.a'), ('M1.b', 'L2.a')])
    assert get_connected_num(ML, 'M1', 'L', M_COMP) == 2


def test_with_aux_edge():
    # Aux edge should not be counted
    M_COMP = Component(['a', 'b'], aux_edges=[('a', 'b', 'cis')])
    ML = Assembly({'M1': 'M'})
    assert get_connected_num(ML, 'M1', 'L', M_COMP) == 0


def test_with_other_kind_of_component():
    # Only bindsites of the specified kind ('L') should be counted
    M_COMP = Component(['a', 'b'])
    MX = Assembly({'M1': 'M', 'X1': 'X'}, [('M1.a', 'X1.a')])
    assert get_connected_num(MX, 'M1', 'L', M_COMP) == 0


def test_with_mix_of_kinds():
    # Only bindsites of the specified kind ('L') should be counted
    M_COMP = Component(['a', 'b'])
    MLX = Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},
                    [('M1.a', 'L1.a'), ('M1.b', 'X1.a')])
    assert get_connected_num(MLX, 'M1', 'L', M_COMP) == 1


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
