import pytest

from recsa.pipelines.bondset_enumeration import parse_sym_ops


def test_with_sym_maps():
    input_data = {
        'sym_maps': {
            'C2': {1: 4, 2: 3, 3: 2, 4: 1}
        }
    }
    expected = {
        'C2': {1: 4, 2: 3, 3: 2, 4: 1}
    }
    assert parse_sym_ops(input_data) == expected


def test_with_sym_perms():
    input_data = {
        'sym_perms': {
            'C3': [[1, 2, 3]]
        }
    }
    expected = {
        'C3': {1: 2, 2: 3, 3: 1}
    }
    assert parse_sym_ops(input_data) == expected


def test_with_both_sym_maps_and_sym_perms():
    input_data = {
        'sym_maps': {
            'C2': {1: 4, 2: 3, 3: 2, 4: 1}
        },
        'sym_perms': {
            'C3': [[1, 2, 3]]
        }
    }
    # sym_maps should be prioritized
    expected = {
        'C2': {1: 4, 2: 3, 3: 2, 4: 1}
    }
    assert parse_sym_ops(input_data) == expected


def test_with_no_sym_ops():
    input_data = {}  # type: ignore
    assert parse_sym_ops(input_data) is None


if __name__ == '__main__':
    pytest.main(['-vv', __file__])