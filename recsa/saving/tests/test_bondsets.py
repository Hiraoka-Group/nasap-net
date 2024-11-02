import pytest
import yaml

from recsa import save_bondsets


def test_typical_case(tmp_path):
    BONDSETS = [
        ['2'], ['1', '2'], ['1'], ['1', '3', '2']
    ]
    EXPECTED_BONDSETS = [
        ['1'], ['2'], ['1', '2'], ['1', '2', '3']
    ]

    save_bondsets(BONDSETS, tmp_path / "bondsets.yaml")

    with open(tmp_path / "bondsets.yaml") as f:
        loaded_bondsets = yaml.safe_load(f)

    assert loaded_bondsets == EXPECTED_BONDSETS


def test_overwrite_false(tmp_path):
    BONDSETS = [['1']]
    NEW_BONDSETS = [['2']]
    EXPECTED_BONDSETS = [['1']]

    save_bondsets(BONDSETS, tmp_path / "bondsets.yaml")
    save_bondsets(NEW_BONDSETS, tmp_path / "bondsets.yaml", overwrite=False)

    with open(tmp_path / "bondsets.yaml") as f:
        loaded_bondsets = yaml.safe_load(f)

    assert loaded_bondsets == EXPECTED_BONDSETS


def test_overwrite_true(tmp_path):
    BONDSETS = [['1']]
    NEW_BONDSETS = [['2']]
    EXPECTED_BONDSETS = [['2']]

    save_bondsets(BONDSETS, tmp_path / "bondsets.yaml")
    save_bondsets(NEW_BONDSETS, tmp_path / "bondsets.yaml", overwrite=True)

    with open(tmp_path / "bondsets.yaml") as f:
        loaded_bondsets = yaml.safe_load(f)

    assert loaded_bondsets == EXPECTED_BONDSETS


def test_bond_ordering(tmp_path):
    BONDSETS = [['2', '3', '1']]
    EXPECTED_BONDSETS = [['1', '2', '3']]

    save_bondsets(BONDSETS, tmp_path / "bondsets.yaml")

    with open(tmp_path / "bondsets.yaml") as f:
        loaded_bondsets = yaml.safe_load(f)

    assert loaded_bondsets == EXPECTED_BONDSETS


def test_bondset_ordering_by_alphabet(tmp_path):
    BONDSETS = [['2'], ['3'], ['1']]
    EXPECTED_BONDSETS = [['1'], ['2'], ['3']]

    save_bondsets(BONDSETS, tmp_path / "bondsets.yaml")

    with open(tmp_path / "bondsets.yaml") as f:
        loaded_bondsets = yaml.safe_load(f)

    assert loaded_bondsets == EXPECTED_BONDSETS


def test_bondset_ordering_by_length(tmp_path):
    # The bondsets are sorted by length first, 
    # then by the elements in the bondset
    BONDSETS = [['1', '2', '3'], ['4'], ['5', '6']]
    EXPECTED_BONDSETS = [['4'], ['5', '6'], ['1', '2', '3']]

    save_bondsets(BONDSETS, tmp_path / "bondsets.yaml")

    with open(tmp_path / "bondsets.yaml") as f:
        loaded_bondsets = yaml.safe_load(f)

    assert loaded_bondsets == EXPECTED_BONDSETS


def test_test_zero_padded_numbers(tmp_path):
    # Test to ensure that zero-padded numbers are all quoted in the output
    
    # In YAML 1.1, scalars starting with a zero are resolved as 
    # octal numbers if they only contain 0-7 unless they are quoted.
    # So, in order to represent numbers like '08' and '09' as strings,
    # they need to be quoted. This is why the PyYAML library quotes
    # numbers like '01' and '07' when dumping them as strings.

    # On the other hand, since numbers like '08' and '09' are not valid 
    # octal numbers, PyYAML does not need to quote them. This is why
    # PyYAML does not quote numbers like '08' and '09' when dumping them
    # as strings.

    # YAML 1.2 changed the rules for octal numbers, and now scalars starting
    # with a zero are not resolved as octal numbers but as integers. This 
    # means all scalars like '01', '07', '08', and '09' need to be quoted
    # in order to represent them as strings.

    # Since we prefer consistency in the output, we decided to use the
    # CoreDumper from the yamlcore library, which implements the YAML 1.2 
    # specification. As a result, all scalars starting with a zero are
    # quoted in the output.

    BONDSETS = {frozenset({'07', '08', '09', '10'})}
    EXPECTED_TEXT = "- ['07', '08', '09', '10']\n"

    save_bondsets(BONDSETS, tmp_path / "bondsets.yaml")

    with open(tmp_path / "bondsets.yaml") as f:
        loaded_text = f.read()

    assert loaded_text == EXPECTED_TEXT


if __name__ == "__main__":
    pytest.main(['-vv', __file__])
