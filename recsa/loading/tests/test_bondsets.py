import pytest
import yaml

from recsa.loading import load_bondsets


# Helper function
def write_bondsets_to_file(tmp_path, bondsets):
    bondsets_file = tmp_path / 'bondsets.yaml'
    with bondsets_file.open('w') as f:
        yaml.dump(bondsets, f)
    return bondsets_file


def test_typical_case(tmp_path):
    BONDSETS = [['1'], ['1', '2']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    assert loaded == BONDSETS


def test_path_obj_input(tmp_path):
    BONDSETS = [['1'], ['1', '2']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)  # input is Path object
    assert loaded == BONDSETS


def test_str_input(tmp_path):
    BONDSETS = [['1'], ['1', '2']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(str(bondsets_file))  # input is str
    assert loaded == BONDSETS


def test_return_type_is_list(tmp_path):
    BONDSETS: list[list] = []
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    assert isinstance(loaded, list)


def test_type_of_bondsets_is_list(tmp_path):
    BONDSETS = [['1'], ['1', '2']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    for bondset in loaded:
        assert isinstance(bondset, list)


def test_type_of_bonds_is_str(tmp_path):
    BONDSETS = [['1'], ['1', '2']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    for bondset in loaded:
        for bond in bondset:
            assert isinstance(bond, str)


def test_convert_int_to_str(tmp_path):
    BONDSETS = [[1], [1, 2]]  # input is int, but should be str
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    assert loaded == [['1'], ['1', '2']]


def test_bondset_order_preserved_1(tmp_path):
    BONDSETS = [['2'], ['1']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    # The order of the bondsets should be preserved
    assert loaded == [['2'], ['1']]


def test_bondset_order_preserved_2(tmp_path):
    BONDSETS = [['1', '2'], ['1']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    # The order of the bondsets should be preserved
    # even if the bondsets have different lengths.
    assert loaded == [['1', '2'], ['1']]

if __name__ == '__main__':
    pytest.main(['-vv', __file__])
