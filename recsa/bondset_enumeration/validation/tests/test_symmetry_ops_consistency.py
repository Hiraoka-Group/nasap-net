import pytest

from recsa.bondset_enumeration import (RecsaMapCyclicInconsistencyError,
                                       validate_symmetry_ops_consistency)


def test_validate_symmetry_ops_consistency_valid():
    ops_by_map = {
        'op1': {'1': '2', '2': '3', '3': '1'},
        'op2': {'1': '3', '2': '1', '3': '2'}
    }
    ops_by_perms = {
        'op1': {'1': '2', '2': '3', '3': '1'},
        'op2': {'1': '3', '2': '1', '3': '2'}
    }
    # No error should be raised
    validate_symmetry_ops_consistency(ops_by_map, ops_by_perms)


def test_validate_symmetry_ops_consistency_extra_ops_by_map():
    ops_by_map = {
        'op1': {'1': '2', '2': '3', '3': '1'},
        'op2': {'1': '3', '2': '1', '3': '2'},
        'op3': {'1': '2', '2': '3', '3': '1'}
    }
    ops_by_perms = {
        'op1': {'1': '2', '2': '3', '3': '1'},
        'op2': {'1': '3', '2': '1', '3': '2'}
    }
    with pytest.raises(RecsaMapCyclicInconsistencyError):
        validate_symmetry_ops_consistency(ops_by_map, ops_by_perms)


def test_validate_symmetry_ops_consistency_extra_ops_by_perms():
    ops_by_map = {
        'op1': {'1': '2', '2': '3', '3': '1'},
        'op2': {'1': '3', '2': '1', '3': '2'}
    }
    ops_by_perms = {
        'op1': {'1': '2', '2': '3', '3': '1'},
        'op2': {'1': '3', '2': '1', '3': '2'},
        'op3': {'1': '2', '2': '3', '3': '1'}
    }
    with pytest.raises(RecsaMapCyclicInconsistencyError):
        validate_symmetry_ops_consistency(ops_by_map, ops_by_perms)


def test_validate_symmetry_ops_consistency_inconsistent_mapping():
    ops_by_map = {
        'op1': {'1': '2', '2': '3', '3': '1'},
        'op2': {'1': '3', '2': '1', '3': '2'}
    }
    ops_by_perms = {
        'op1': {'1': '2', '2': '3', '3': '1'},
        'op2': {'1': '1', '2': '2', '3': '3'}  # inconsistent mapping
    }
    with pytest.raises(RecsaMapCyclicInconsistencyError):
        validate_symmetry_ops_consistency(ops_by_map, ops_by_perms)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
