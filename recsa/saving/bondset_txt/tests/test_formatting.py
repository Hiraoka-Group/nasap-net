import pytest

from recsa.saving.bondset_txt import format_bond_subsets


def test_format_bond_subsets():
    bond_subsets = {
        frozenset(['1', '2']),
        frozenset(['1', '3']),
        frozenset(['4']),
    }
    
    expected_output = [
        "4",
        "1, 2",
        "1, 3",
    ]
    
    assert list(format_bond_subsets(bond_subsets)) == expected_output


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
