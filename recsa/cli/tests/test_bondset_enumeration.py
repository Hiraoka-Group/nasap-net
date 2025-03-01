import os

import pytest
import yaml
from click.testing import CliRunner

from recsa.cli.commands import run_bond_subset_pipeline


def test_cli_command_a(tmp_path):
    runner = CliRunner()

    INPUT_DATA = {
        'bonds': [1, 2, 3, 4],
        'adj_bonds': {
            1: {2},
            2: {1, 3},
            3: {2, 4},
            4: {3}}
        }

    with runner.isolated_filesystem(temp_dir=tmp_path) as td:
        input_path = os.path.join(td, 'input.yaml')
        output_path = os.path.join(td, 'output.yaml')

        with open(input_path, 'w') as f:
            yaml.safe_dump(INPUT_DATA, f)
        
        result = runner.invoke(
            run_bond_subset_pipeline,
            ['--input', input_path, '--output', output_path]
        )

        assert result.exit_code == 0
        assert os.path.exists(output_path)


if __name__ == '__main__':
    pytest.main(['-v', __file__])
