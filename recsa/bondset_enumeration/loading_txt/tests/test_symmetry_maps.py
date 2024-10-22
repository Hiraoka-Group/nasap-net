import pytest

from recsa import RecsaParsingError
from recsa.bondset_enumeration import parse_symmetry_maps


def test_parse_symmetry_maps():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'sigma_1: 1->1, 2->3, 3->2'
    ]
    expected_result = {
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
    assert parse_symmetry_maps(lines, bonds) == expected_result


def test_parse_symmetry_maps_missing_colon():
    bonds = ['1', '2', '3']
    lines = [
        'C_3  1->2, 2->3, 3->1',  # missing colon
        'sigma_1: 1->1, 2->3, 3->2'
    ]
    with pytest.raises(RecsaParsingError, match='Missing colon'):
        parse_symmetry_maps(lines, bonds)


def test_parse_symmetry_maps_multiple_colons():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'sigma_1: 1->1: 2->3: 3->2'  # multiple colons
    ]
    with pytest.raises(RecsaParsingError, match='Multiple colons'):
        parse_symmetry_maps(lines, bonds)

    
def test_parse_symmetry_maps_duplicate_symmetry_op_name():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'C_3: 1->2, 2->3, 3->1'  # duplicate symmetry operation name
    ]
    with pytest.raises(RecsaParsingError, match='Duplicate symmetry operation name'):
        parse_symmetry_maps(lines, bonds)


def test_parse_symmetry_maps_missing_arrow():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'sigma_1: 1->1, 2->3, 3-2'  # missing arrow
    ]
    with pytest.raises(RecsaParsingError, match='Missing "->"'):
        parse_symmetry_maps(lines, bonds)


def test_parse_symmetry_maps_multiple_arrows():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'sigma_1: 1->1, 2->3->2'  # multiple arrows
    ]
    with pytest.raises(RecsaParsingError, match='Multiple "->"'):
        parse_symmetry_maps(lines, bonds)


def test_parse_symmetry_maps_unknown_source_bond():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'sigma_1: 1->1, 2->3, 4->2'  # unknown source bond "4"
    ]
    with pytest.raises(RecsaParsingError, match='Unknown source bond'):
        parse_symmetry_maps(lines, bonds)


def test_parse_symmetry_maps_unknown_target_bond():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'sigma_1: 1->1, 2->3, 3->4'  # unknown target bond "4"
    ]
    with pytest.raises(RecsaParsingError, match='Unknown target bond'):
        parse_symmetry_maps(lines, bonds)


def test_parse_symmetry_maps_missing_source_bond():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'sigma_1: 1->1, 2->3'  # missing source bond "3"
    ]
    with pytest.raises(RecsaParsingError, match='Mapping for bond "3" is missing'):
        parse_symmetry_maps(lines, bonds)


def test_parse_symmetry_maps_missing_target_bond():
    bonds = ['1', '2', '3']
    lines = [
        'C_3: 1->2, 2->3, 3->1',
        'sigma_1: 1->1, 2->1, 3->2'  # No bond maps to "3"
    ]
    with pytest.raises(RecsaParsingError, match='No bond maps to "3"'):
        parse_symmetry_maps(lines, bonds)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
