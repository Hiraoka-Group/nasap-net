import pytest

from recsa import RecsaParsingError
from recsa.bondset_enumeration import parse_adj_bonds


def test_parse_adj_bonds_valid():
    # M2L3 linear assembly (L-M-L-M-L) with bonds 1, 2, 3, and 4.
    bonds = ['1', '2', '3', '4']
    lines = [
        '1: 2',
        '2: 1, 3,',
        '3: 2, 4',
        '4: 3'
    ]
    expected_result = {
        '1': {'2'},
        '2': {'1', '3'},
        '3': {'2', '4'},
        '4': {'3'},
    }
    assert parse_adj_bonds(lines, bonds) == expected_result


def test_parse_adj_bonds_missing_colon():
    bonds = ['1', '2', '3']
    lines = [
        '1 2',  # missing colon
        '2: 1, 3',
        '3: 2'
    ]
    with pytest.raises(RecsaParsingError, match='Missing colon'):
        parse_adj_bonds(lines, bonds)


def test_parse_adj_bonds_multiple_colons():
    bonds = ['1', '2', '3']
    lines = [
        '1: 2, 3',
        '2: 1: 3',  # multiple colons
        '3: 2'
    ]
    with pytest.raises(RecsaParsingError, match='Multiple colons'):
        parse_adj_bonds(lines, bonds)


def test_parse_adj_bonds_unknown_bond_name():
    bonds = ['1', '2', '3']
    lines = [
        '1: 2',
        '2: 1, 3',
        '3: 2',
        '4: 3'  # unknown bond name "4"
    ]
    with pytest.raises(RecsaParsingError, match='Unknown bond name'):
        parse_adj_bonds(lines, bonds)


def test_parse_adj_bonds_duplicate_bond_name():
    bonds = ['1', '2', '3']
    lines = [
        '1: 2',
        '2: 1, 3',
        '3: 2',
        '1: 3'  # duplicate bond name "1"
    ]
    with pytest.raises(RecsaParsingError, match='Duplicate bond name'):
        parse_adj_bonds(lines, bonds)


def test_parse_adj_bonds_empty_bond_name():
    bonds = ['1', '2', '3']
    lines = [
        '1: 2, 3',
        '2: 1, , 3',  # invalid bond name (empty bond name)
        '3: 2'
    ]
    with pytest.raises(RecsaParsingError, match='Empty bond name'):
        parse_adj_bonds(lines, bonds)


def test_parse_adj_bonds_unknown_bond_name_1():
    bonds = ['1', '2', '3']
    lines = [
        '1: 2',
        '2: 1, 3',
        '3: 2, 4'  # unknown bond name "4"
    ]
    with pytest.raises(RecsaParsingError, match='Unknown adjacent bond name'):
        parse_adj_bonds(lines, bonds)


def test_parse_adj_bonds_unknown_bond_name_2():
    bonds = ['1', '2', '3']
    lines = [
        '1: 2',
        '2: 1 3',  # invalid bond name
        '3: 2'
        # "1 3" is considered as one bond, and not included in bonds
    ]
    with pytest.raises(RecsaParsingError, match='Unknown adjacent bond name'):
        parse_adj_bonds(lines, bonds)


def test_parse_adj_bonds_duplicate_adjacent_bonds():
    bonds = ['1', '2']
    lines = [
        '1: 2',
        '2: 1, 1'  # Duplicate adjacent bonds should be silently ignored.
    ]
    parse_adj_bonds(lines, bonds)  # no error should be raised


def test_parse_adj_bonds_missing_bond():
    bonds = ['1', '2', '3']
    lines = [
        '1: 2',
        '2: 1',
        # missing bond "3"
    ]
    with pytest.raises(RecsaParsingError, match='No adjacent bonds for bond "3"'):
        parse_adj_bonds(lines, bonds)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
