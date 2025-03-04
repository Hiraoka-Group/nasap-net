import os

import pytest
import yaml
from click.testing import CliRunner

from recsa import Assembly
from recsa.cli.main import main


def test_enum_bond_subsets(tmp_path):
    runner = CliRunner()

    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'adj_bonds': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3}},
        'sym_maps': {
            'C2': {1: 4, 2: 3, 3: 2, 4: 1}
        }
    }

    EXPECTED = [[1], [2], [1, 2], [2, 3], [1, 2, 3], [1, 2, 3, 4]]

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        input_path = os.path.join(td, 'input.yaml')
        output_path = os.path.join(td, 'output.yaml')

        with open(input_path, 'w') as f:
            yaml.safe_dump(INPUT_DATA, f)
        
        result = runner.invoke(
            main,
            ['enumerate-bond-subsets', input_path, output_path]
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)

        with open(output_path, 'r') as f:
            actual_output = yaml.safe_load(f)

        assert actual_output == EXPECTED


def test_bondsets_to_assemblies(tmp_path):
    runner = CliRunner()

    BONDSETS_DATA = {
        0: [1],
        1: [1, 2],
        2: [2, 3],
        3: [1, 2, 3],
        4: [1, 2, 3, 4]
    }

    STRUCTURE_DATA = {
        'comp_id_to_kind': {
            'M1': 'M',
            'M2': 'M',
            'L1': 'L',
            'L2': 'L',
            'L3': 'L'
        },
        'bond_id_to_bindsites': {
            1: ['L1.b', 'M1.a'],
            2: ['M1.b', 'L2.a'],
            3: ['L2.b', 'M2.a'],
            4: ['M2.b', 'L3.a']
        }
    }

    EXPECTED = {
        0: Assembly({'L1': 'L', 'M1': 'M'}, [('L1.b', 'M1.a')]),
        1: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a')]),
        2: Assembly(
            {'M1': 'M', 'L2': 'L', 'M2': 'M'},
            [('M1.b', 'L2.a'), ('L2.b', 'M2.a')]),
        3: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a')]),
        4: Assembly(
            {'L1': 'L', 'M1': 'M', 'L2': 'L', 'M2': 'M', 'L3': 'L'},
            [('L1.b', 'M1.a'), ('M1.b', 'L2.a'), ('L2.b', 'M2.a'), 
             ('M2.b', 'L3.a')])
    }

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        bondsets_path = os.path.join(td, 'bondsets.yaml')
        structure_data_path = os.path.join(td, 'structure_data.yaml')
        output_path = os.path.join(td, 'output.yaml')

        with open(bondsets_path, 'w') as f:
            yaml.safe_dump(BONDSETS_DATA, f)

        with open(structure_data_path, 'w') as f:
            yaml.safe_dump(STRUCTURE_DATA, f)

        result = runner.invoke(
            main,
            ['bondsets-to-assemblies', bondsets_path, structure_data_path, 
             output_path]
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)

        with open(output_path, 'r') as f:
            actual_output = yaml.safe_load(f)
        
        assert actual_output == EXPECTED


if __name__ == '__main__':
    pytest.main(['-v', __file__])
