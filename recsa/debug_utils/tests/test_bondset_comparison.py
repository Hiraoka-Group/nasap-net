import pytest

from recsa.debug_utils import compare_bondsets_under_sym_ops


def test_same():
    BONDSET1 = [['01']]
    BONDSET2 = [['01']]
    SYM_OPS = None
    result = compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)
    assert result == (set(), set())


def test_same_under_sym_ops():
    BONDSET1 = [['01']]
    BONDSET2 = [['02']]
    SYM_OPS = {'foo': {'01': '02', '02': '01'}}
    result = compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)
    assert result == (set(), set())


def test_same_but_different_order():
    BONDSET1 = [['01', '02']]
    BONDSET2 = [['02', '01']]
    SYM_OPS = None
    result = compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)
    assert result == (set(), set())


def test_same_with_multiple_sym_ops():
    BONDSET1 = [['01'], ['03']]
    BONDSET2 = [['02'], ['04']]
    SYM_OPS = {'foo': {'01': '02', '02': '01', '03': '03', '04': '04'},
               'bar': {'01': '01', '02': '02', '03': '04', '04': '03'}}
    # 02 is equivalent to 01 under 'foo' and 04 is equivalent to 03 under 'bar'.
    result = compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)
    assert result == (set(), set())


def test_different():
    BONDSET1 = [['01']]
    BONDSET2 = [['02']]
    SYM_OPS = None
    result = compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)
    assert result == ({frozenset({'01'})}, {frozenset({'02'})})


def test_different_under_sym_ops():
    BONDSET1 = [['01']]
    BONDSET2 = [['03']]
    SYM_OPS = {'foo': {'01': '02', '02': '01', '03': '03'}}
    result = compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)
    assert result == ({frozenset({'01'})}, {frozenset({'03'})})


def test_duplicate_bond():
    BONDSET1 = [['01', '01']]  # Duplicate bond.
    BONDSET2 = [['02']]
    SYM_OPS = None
    with pytest.raises(ValueError):
        compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)


def test_duplicate_bondset():
    BONDSET1 = [['01'], ['01']]  # Duplicate bondset.
    BONDSET2 = [['01']]
    SYM_OPS = None
    with pytest.raises(ValueError):
        compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)


def test_duplicate_bondset_under_sym_ops():
    BONDSET1 = [['01'], ['02']]  # Duplicate bondset under symmetry operations.
    BONDSET2 = [['01']]
    SYM_OPS = {'foo': {'01': '02', '02': '01'}}
    with pytest.raises(ValueError):
        compare_bondsets_under_sym_ops(BONDSET1, BONDSET2, SYM_OPS)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])