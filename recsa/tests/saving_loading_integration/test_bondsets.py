import pytest

from recsa import load_bondsets, save_bondsets


def test_typical_case(tmp_path):
    BONDSETS = [
        ['1'], ['2'], ['1', '2'], ['1', '2', '3']
    ]
    EXPECTED_BONDSETS = {
        0: {'1'}, 1: {'2'}, 2: {'1', '2'}, 3: {'1', '2', '3'}
    }

    save_bondsets(BONDSETS, tmp_path / "bondsets.json")
    loaded_bondsets = load_bondsets(tmp_path / "bondsets.json")

    assert loaded_bondsets == EXPECTED_BONDSETS


if __name__ == "__main__":
    pytest.main(['-v', __file__])
