import pytest

from recsa.bondset_enumeration import (RecsaMapCyclicInconsistencyError,
                                       enum_bond_subsets_from_file)


# ============================================================
# test enum_bond_subsets_from_file 1
# Triangle with three bonds: 1, 2, 3
# ============================================================
def test_enum_bond_subsets_from_file_1_using_map(tmp_path):
    # Triangle with 3 bonds
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3]
bond_to_adjs:
    1: [2, 3]
    2: [1, 3]
    3: [1, 2]
sym_mappings:
    C_3: {1: 2, 2: 3, 3: 1}
    C_3^2: {1: 3, 2: 1, 3: 2}
    sigma_1: {1: 1, 2: 3, 3: 2}
    sigma_2: {1: 3, 2: 2, 3: 1}
    sigma_3: {1: 2, 2: 1, 3: 3}
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)
    result = enum_bond_subsets_from_file(p)

    assert result == {
        frozenset({'1'}), 
        frozenset({'1', '2'}), 
        frozenset({'1', '2', '3'})}


def test_enum_bond_subsets_from_file_1_using_cyclic_perm(tmp_path):
    # Triangle with 3 bonds
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3]
bond_to_adjs:
    1: [2, 3]
    2: [1, 3]
    3: [1, 2]
sym_perms:
    C_3: [[1, 2, 3]]
    C_3^2: [[1, 3, 2]]
    sigma_1: [[1], [2, 3]]
    sigma_2: [[1, 3], [2]]
    sigma_3: [[1, 2], [3]]
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)
    result = enum_bond_subsets_from_file(p)

    assert result == {
        frozenset({'1'}), 
        frozenset({'1', '2'}), 
        frozenset({'1', '2', '3'})}


def test_enum_bond_subsets_from_file_1_using_both(tmp_path):
    # Triangle with 3 bonds
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3]
bond_to_adjs:
    1: [2, 3]
    2: [1, 3]
    3: [1, 2]
sym_mappings:
    C_3: {1: 2, 2: 3, 3: 1}
    C_3^2: {1: 3, 2: 1, 3: 2}
    sigma_1: {1: 1, 2: 3, 3: 2}
    sigma_2: {1: 3, 2: 2, 3: 1}
    sigma_3: {1: 2, 2: 1, 3: 3}
sym_perms:
    C_3: [[1, 2, 3]]
    C_3^2: [[1, 3, 2]]
    sigma_1: [[1], [2, 3]]
    sigma_2: [[1, 3], [2]]
    sigma_3: [[1, 2], [3]]
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)
    result = enum_bond_subsets_from_file(p)

    assert result == {
        frozenset({'1'}), 
        frozenset({'1', '2'}), 
        frozenset({'1', '2', '3'})}


def test_enum_bond_subsets_from_file_1_with_inconsistent_map_and_cyclic(tmp_path):
    # Triangle with 3 bonds
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3]
bond_to_adjs:
    1: [2, 3]
    2: [1, 3]
    3: [1, 2]
sym_mappings:
    C_3: {1: 2, 2: 3, 3: 1}
    C_3^2: {1: 3, 2: 1, 3: 2}
    sigma_1: {1: 1, 2: 3, 3: 2}
    sigma_2: {1: 3, 2: 2, 3: 1}
    sigma_3: {1: 2, 2: 1, 3: 3}
sym_perms:
    C_3: [[1, 2, 3]]
    C_3^2: [[1, 3, 2]]
    sigma_1: [[1], [2, 3]]
    sigma_2: [[1, 3], [2]]
    sigma_3: [[1, 3], [2]]  # inconsistent with map
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)

    # assert error
    with pytest.raises(RecsaMapCyclicInconsistencyError):
        enum_bond_subsets_from_file(p)


# ============================================================
# test enum_bond_subsets_from_file 2
# Linear assembly M2L3: L-M-L-M-L with bonds 1, 2, 3, 4
# ============================================================
def test_enum_bond_subsets_from_file_2_using_map(tmp_path):
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3, 4]
bond_to_adjs:
    1: [2]
    2: [1, 3]
    3: [2, 4]
    4: [3]
sym_mappings:
    C2: {1: 4, 2: 3, 3: 2, 4: 1}
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)
    result = enum_bond_subsets_from_file(p)

    assert result == {
        frozenset({'1'}), frozenset({'2'}),
        frozenset({'1', '2'}), frozenset({'2', '3'}),
        frozenset({'1', '2', '3'}),
        frozenset({'1', '2', '3', '4'})}


def test_enum_bond_subsets_from_file_2_using_cyclic_perm(tmp_path):
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3, 4]
bond_to_adjs:
  1: [2]
  2: [1, 3]
  3: [2, 4]
  4: [3]
sym_perms:
  C2: [[1, 4], [2, 3]]
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)
    result = enum_bond_subsets_from_file(p)

    assert result == {
        frozenset({'1'}), frozenset({'2'}),
        frozenset({'1', '2'}), frozenset({'2', '3'}),
        frozenset({'1', '2', '3'}),
        frozenset({'1', '2', '3', '4'})}


def test_enum_bond_subsets_from_file_2_using_both(tmp_path):
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3, 4]
bond_to_adjs:
    1: [2]
    2: [1, 3]
    3: [2, 4]
    4: [3]
sym_mappings:
    C2: {1: 4, 2: 3, 3: 2, 4: 1}
sym_perms:
    C2: [[1, 4], [2, 3]]
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)
    result = enum_bond_subsets_from_file(p)

    assert result == {
        frozenset({'1'}), frozenset({'2'}),
        frozenset({'1', '2'}), frozenset({'2', '3'}),
        frozenset({'1', '2', '3'}),
        frozenset({'1', '2', '3', '4'})}


def test_enum_bond_subsets_from_file_2_with_inconsistent_map_and_cyclic(tmp_path):
    # M2L3 linear: L-M-L-M-L
    # bonds: 1, 2, 3, 4 from left to right
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3, 4]
bond_to_adjs:
    1: [2]
    2: [1, 3]
    3: [2, 4]
    4: [3]
sym_mappings:
    C2: {1: 4, 2: 3, 3: 2, 4: 1}
sym_perms:
    C2: [[1, 2], [3, 4]]  # inconsistent with map
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)

    # assert error
    with pytest.raises(RecsaMapCyclicInconsistencyError):
        enum_bond_subsets_from_file(p)


# ============================================================
# test enum_bond_subsets_from_file 3
# M4L4 square assembly with bonds 1, 2, 3, 4, 5, 6, 7, 8
# 
#  M4-(6)-L3-(5)-M3
#  |             |
# (7)           (4)
#  |             |
#  L4            L2
#  |             |
# (8)           (3)
#  |             |
#  M1-(1)-L1-(2)-M2
# 
# ============================================================

def test_enum_bond_subsets_from_file_3_using_map(tmp_path):
    # M4L4 square
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3, 4, 5, 6, 7, 8]
bond_to_adjs:
    1: [8, 2]
    2: [1, 3]
    3: [2, 4]
    4: [3, 5]
    5: [4, 6]
    6: [5, 7]
    7: [6, 8]
    8: [7, 1]
sym_mappings:
    C_4: {1: 3, 2: 4, 3: 5, 4: 6, 5: 7, 6: 8, 7: 1, 8: 2}
    C_2: {1: 5, 2: 6, 3: 7, 4: 8, 5: 1, 6: 2, 7: 3, 8: 4}
    C_4^3: {1: 7, 2: 8, 3: 1, 4: 2, 5: 3, 6: 4, 7: 5, 8: 6}
    C_2x: {1: 2, 2: 1, 3: 8, 4: 7, 5: 6, 6: 5, 7: 4, 8: 3}
    C_2y: {1: 6, 2: 5, 3: 4, 4: 3, 5: 2, 6: 1, 7: 8, 8: 7}
    C_2(1): {1: 4, 2: 3, 3: 2, 4: 1, 5: 8, 6: 7, 7: 6, 8: 5}
    C_2(2): {1: 8, 2: 7, 3: 6, 4: 5, 5: 4, 6: 3, 7: 2, 8: 1}
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)
    result = enum_bond_subsets_from_file(p)

    expected_result = {
        frozenset({'1',}),
        frozenset({'1', '2'}), frozenset({'1', '8'}),
        frozenset({'1', '2', '3'}),
        frozenset({'1', '2', '3', '4'}), frozenset({'1', '2', '3', '8'}),
        frozenset({'1', '2', '3', '4', '5'}),
        frozenset({'1', '2', '3', '4', '5', '6'}),
        frozenset({'1', '2', '3', '4', '5', '8'}),
        frozenset({'1', '2', '3', '4', '5', '6', '7'}),
        frozenset({'1', '2', '3', '4', '5', '6', '7', '8'}),   
    }
   
    assert result == expected_result



def test_enum_bond_subsets_from_file_3_using_cyclic_perm(tmp_path):
    # M4L4 square
    INPUT_FILE_CONTENTS = """
bonds: [1, 2, 3, 4, 5, 6, 7, 8]
bond_to_adjs:
    1: [8, 2]
    2: [1, 3]
    3: [2, 4]
    4: [3, 5]
    5: [4, 6]
    6: [5, 7]
    7: [6, 8]
    8: [7, 1]
sym_perms:
    C_4: [[1, 3, 5, 7], [2, 4, 6, 8]]
    C_2: [[1, 5], [2, 6], [3, 7], [4, 8]]
    C_4^3: [[1, 7, 5, 3], [2, 8, 6, 4]]
    C_2x: [[1, 2], [3, 8], [4, 7], [5, 6]]
    C_2y: [[1, 6], [2, 5], [3, 4], [7, 8]]
    C_2(1): [[1, 4], [2, 3], [5, 8], [6, 7]]
    C_2(2): [[1, 8], [2, 7], [3, 6], [4, 5]]
"""
    p = tmp_path / 'input.yaml'
    p.write_text(INPUT_FILE_CONTENTS)
    result = enum_bond_subsets_from_file(p)

    expected_result = {
        frozenset({'1',}),
        frozenset({'1', '2'}), frozenset({'1', '8'}),
        frozenset({'1', '2', '3'}),
        frozenset({'1', '2', '3', '4'}), frozenset({'1', '2', '3', '8'}),
        frozenset({'1', '2', '3', '4', '5'}),
        frozenset({'1', '2', '3', '4', '5', '6'}),
        frozenset({'1', '2', '3', '4', '5', '8'}),
        frozenset({'1', '2', '3', '4', '5', '6', '7'}),
        frozenset({'1', '2', '3', '4', '5', '6', '7', '8'}),   
    }

    assert result == expected_result


if __name__ == '__main__':
    pytest.main(['-v', __file__])
