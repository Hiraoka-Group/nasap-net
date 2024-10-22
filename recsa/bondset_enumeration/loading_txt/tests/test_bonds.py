import re

import pytest

from recsa import RecsaParsingError
from recsa.bondset_enumeration import parse_bonds


def test_parse_bonds_valid():
    lines = ['1, 2, 3']
    expected_result = {'1', '2', '3'}
    assert parse_bonds(lines) == expected_result

    # Leading and trailing whitespaces and commas should be removed.
    lines = [',, 1, 2, 3, ']
    assert parse_bonds(lines) == expected_result


def test_parse_bonds_empty():
    lines = [None]
    with pytest.raises(
            RecsaParsingError, match=re.escape('Empty [bonds] section')):
        parse_bonds(lines)  # type: ignore
    
    lines = ['  ']  # type: ignore
    with pytest.raises(
            RecsaParsingError, match=re.escape('Empty [bonds] section')):
        parse_bonds(lines)  # type: ignore


def test_parse_bonds_invalid_bond_name():
    line = ['1, 2, 3, 4 5']
    with pytest.raises(RecsaParsingError, match='Invalid bond name'):
        parse_bonds(line)


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
