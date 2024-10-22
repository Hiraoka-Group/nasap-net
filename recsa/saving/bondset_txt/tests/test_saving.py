import pytest

from recsa.saving.bondset_txt import save_bondsets_as_txt


def test_save_bondsets_as_txt(tmp_path):
    # Create a temporary file path
    output_file = tmp_path / "output.txt"

    # Define the bond subsets
    bond_subsets = {
        frozenset(['1', '2']),
        frozenset(['1', '3']),
        frozenset(['4']),
    }

    # Call the function to save the results
    save_bondsets_as_txt(output_file, bond_subsets)

    # Check if the file was created
    assert output_file.exists()

    # Check the content of the file
    with output_file.open("r") as f:
        lines = f.readlines()

    assert lines == [
        "4\n",
        "1, 2\n",
        "1, 3\n",
    ]


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
