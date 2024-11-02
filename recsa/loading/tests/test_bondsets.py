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
    assert loaded == {i: set(bondset) for i, bondset in enumerate(BONDSETS)}


def test_path_obj_input(tmp_path):
    BONDSETS = [['1'], ['1', '2']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)  # input is Path object
    assert loaded == {i: set(bondset) for i, bondset in enumerate(BONDSETS)}


def test_str_input(tmp_path):
    BONDSETS = [['1'], ['1', '2']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(str(bondsets_file))  # input is str
    assert loaded == {i: set(bondset) for i, bondset in enumerate(BONDSETS)}


def test_type_of_bonds_is_str(tmp_path):
    BONDSETS = [['1'], ['1', '2']]
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    for bondset in loaded.values():
        for bond in bondset:
            assert isinstance(bond, str)


def test_convert_int_to_str(tmp_path):
    BONDSETS = [[1], [1, 2]]  # input is int, but should be str
    bondsets_file = write_bondsets_to_file(tmp_path, BONDSETS)
    loaded = load_bondsets(bondsets_file)
    assert loaded == {0: {'1'}, 1: {'1', '2'}}


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
