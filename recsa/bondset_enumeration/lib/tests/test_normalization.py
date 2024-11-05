import pytest

from recsa.bondset_enumeration import normalize_bondset_under_sym_ops


def test_1():
    BONDSET = {'01'}
    SYM_OPS = {'foo': {'01': '02', '02': '01'}}
    result = normalize_bondset_under_sym_ops(BONDSET, SYM_OPS)
    assert result == {'01'}


def test_2():
    BONDSET = {'02'}
    SYM_OPS = {'foo': {'01': '02', '02': '01'}}
    result = normalize_bondset_under_sym_ops(BONDSET, SYM_OPS)
    assert result == {'01'}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
