from pathlib import Path

import pytest
import yaml

from recsa import enum_bond_subsets_pipeline


def test_triangle(tmp_path):
    input_file = tmp_path / "input.txt"
    output_file = tmp_path / "output.txt"

    input_data = """
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
    input_file.write_text(input_data)

    enum_bond_subsets_pipeline(str(input_file), str(output_file), overwrite=True)

    assert output_file.exists()
    assert output_file.read_text() == """\
- ['1']
- ['1', '2']
- ['1', '2', '3']
"""


DATA_DIR = Path(__file__).parent / "data"

@pytest.mark.parametrize("input_file, expected_output_file", [
    (DATA_DIR / "M4L4_input.yaml", DATA_DIR / "M4L4_output.yaml"),
    (DATA_DIR / "M2L4_input.yaml", DATA_DIR / "M2L4_output.yaml"),
    (DATA_DIR / "M9L6_input.yaml", DATA_DIR / "M9L6_output.yaml"),
])
def test_example_cases(input_file, expected_output_file, tmp_path):
    input_path = tmp_path / "input.yaml"
    output_path = tmp_path / "output.yaml"

    with open(input_file, "r") as f:
        input_data = f.read()
    input_path.write_text(input_data)

    enum_bond_subsets_pipeline(str(input_path), str(output_path), overwrite=True)

    assert output_path.exists()
    
    with open(expected_output_file, "r") as f:
        expected_output = yaml.safe_load(f)
    
    with open(output_path, "r") as f:
        actual_output = yaml.safe_load(f)
    
    assert actual_output == expected_output


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
