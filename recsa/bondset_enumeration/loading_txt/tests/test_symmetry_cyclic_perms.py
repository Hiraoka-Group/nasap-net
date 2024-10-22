import pytest

from recsa import RecsaParsingError
from recsa.bondset_enumeration import parse_symmetry_cyclic_perms


def test_parse_symmetry_cyclic_perms():
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: (1, 2, 3)',
        'sigma_1: (1), (2, 3)'
    ]
    expected_result = {
        'E': {
            '1': '1',
            '2': '2',
            '3': '3'
        },
        'C_3': {
            '1': '2',
            '2': '3',
            '3': '1'
        },
        'sigma_1': {
            '1': '1',
            '2': '3',
            '3': '2'
        }
    }
    assert parse_symmetry_cyclic_perms(lines, bonds) == expected_result


def test_parse_symmetry_cyclic_perms_missing_colon():
    bonds = ['1', '2', '3']
    lines = [
        'E  (1), (2), (3)',  # missing colon
        'C_3: (1, 2, 3)',
        'sigma_1: (1), (2, 3)'
    ]
    with pytest.raises(RecsaParsingError, match='Missing colon'):
        parse_symmetry_cyclic_perms(lines, bonds)


def test_parse_symmetry_cyclic_perms_multiple_colons():
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: (1, 2, 3)',
        'sigma_1: (1), (2, 3): (1)'  # multiple colons
    ]
    with pytest.raises(RecsaParsingError, match='Multiple colons'):
        parse_symmetry_cyclic_perms(lines, bonds)


def test_parse_symmetry_cyclic_perms_invalid_op_name():
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: (1, 2, 3)',
        'sigma 1: (1), (2, 3)'  # invalid symmetry operation name
    ]
    with pytest.raises(RecsaParsingError, match='Invalid symmetry operation name'):
        parse_symmetry_cyclic_perms(lines, bonds)


def test_parse_symmetry_cyclic_perms_duplicate_op_name():
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: (1, 2, 3)',
        'E: (1), (2, 3)'  # duplicate symmetry operation name
    ]
    with pytest.raises(RecsaParsingError, match='Duplicate symmetry operation name'):
        parse_symmetry_cyclic_perms(lines, bonds)


def test_parse_symmetry_cyclic_perms_missing_permutation():
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: 1, 2, 3',  # missing parentheses thus missing permutation
        'sigma_1: (1), (2), (3)'
    ]
    with pytest.raises(RecsaParsingError, match='No permutations in line'):
        parse_symmetry_cyclic_perms(lines, bonds)


def test_parse_symmetry_cyclic_perms_missing_bond():    
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: (1, 2, 3)',
        'sigma_1: (1), (2)'  # missing bond "3"
    ]
    with pytest.raises(RecsaParsingError, match='Bond "3" is missing'):
        parse_symmetry_cyclic_perms(lines, bonds)


def test_parse_symmetry_cyclic_perms_duplicate_bond_1():
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: (1, 2, 3)',
        'sigma_1: (1), (2, 3, 3)'  # duplicate bond "3"
    ]
    with pytest.raises(RecsaParsingError, match='Duplicate bond "3"'):
        parse_symmetry_cyclic_perms(lines, bonds)


def test_parse_symmetry_cyclic_perms_duplicate_bond_2():
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: (1, 2, 3)',
        'sigma_1: (1), (2, 3), (3)'  # duplicate bond "3"
    ]
    with pytest.raises(RecsaParsingError, match='Duplicate bond "3"'):
        parse_symmetry_cyclic_perms(lines, bonds)


def test_parse_symmetry_cyclic_perms_unknown_bond():
    bonds = ['1', '2', '3']
    lines = [
        'E: (1), (2), (3)',
        'C_3: (1, 2, 3)',
        'sigma_1: (1), (2, 4), (3)'  # unknown bond "4"
    ]
    with pytest.raises(RecsaParsingError, match='Unknown bond'):
        parse_symmetry_cyclic_perms(lines, bonds)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
