import re
from collections.abc import Iterable
from typing import TypeVar

import pytest
import yaml

from recsa import Assembly, save_assemblies

# ====================
# Helper functions
# ====================

T = TypeVar('T')

def to_set_of_frozenset(
        nested_iterables: Iterable[Iterable[T]]) -> set[frozenset[T]]:
    return {frozenset(item) for item in nested_iterables}


# ====================
# Tests
# ====================

def test_typical_usage(tmp_path):
    MX2 = Assembly({'M1': 'M', 'X1': 'X', 'X2': 'X'},
                   [('M1.a', 'X1.a'), ('M1.b', 'X2.a')])
    L = Assembly({'L1': 'L'})
    MLX = Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},
                   [('M1.a', 'L1.a'), ('M1.b', 'X1.a')])
    ML2 = Assembly({'M1': 'M', 'L1': 'L', 'L2': 'L'},
                   [('M1.a', 'L1.a'), ('M1.b', 'L2.a')])
    assemblies = [MX2, L, MLX, ML2]
    output_file = tmp_path / 'assemblies.yml'

    save_assemblies(assemblies, output_file)

    with open(output_file) as f:
        data = list(yaml.safe_load_all(f))

    assert len(data) == 4
    assert data[0]['index'] == 0
    assert data[0]['assembly'] == MX2
    assert data[1]['index'] == 1
    assert data[1]['assembly'] == L
    assert data[2]['index'] == 2
    assert data[2]['assembly'] == MLX
    assert data[3]['index'] == 3
    assert data[3]['assembly'] == ML2


def test_single_assembly(tmp_path):
    MX = Assembly({'M1': 'M', 'X1': 'X'}, [('M1.a', 'X1.a')])
    output_file = tmp_path / 'assemblies.yml'

    save_assemblies([MX], output_file)

    with open(output_file) as f:
        data = list(yaml.safe_load_all(f))

    assert len(data) == 1
    assert data[0]['index'] == 0
    assert data[0]['assembly'] == MX


def test_empty_assembly(tmp_path):
    output_file = tmp_path / 'assemblies.yml'

    save_assemblies([], output_file)

    with open(output_file) as f:
        data = list(yaml.safe_load_all(f))

    assert len(data) == 0


def test_assembly_without_bonds(tmp_path):
    L = Assembly({'L1': 'L'})
    output_file = tmp_path / 'assemblies.yml'

    save_assemblies([L], output_file)

    with open(output_file) as f:
        data = list(yaml.safe_load_all(f))

    assert len(data) == 1
    assert data[0]['index'] == 0
    assert data[0]['assembly'] == L


def test_overwrite(tmp_path):
    output_file = tmp_path / 'assemblies.yml'
    output_file.touch()

    with pytest.raises(FileExistsError):
        save_assemblies([], output_file, overwrite=False)

    save_assemblies([], output_file, overwrite=True)


def test_show_progress_true(capsys, tmp_path):
    assemblies = [Assembly({'M1': 'M', 'X1': 'X'}, [('M1.a', 'X1.a')])
                  for _ in range(3)]
    output_file = tmp_path / 'assemblies.yml'

    save_assemblies(assemblies, output_file, show_progress=True)

    captured = capsys.readouterr()
    expected_output = (
        '\r?\n?Saving assembly 1...\r?\n?'
        'Saving assembly 2...\r?\n?'
        'Saving assembly 3...\r?\n?'
        'All assemblies saved successfully.\r?\n?'
    )
    assert re.match(expected_output, captured.out)


def test_show_progress_false(capsys, tmp_path):
    assemblies = [Assembly({'M1': 'M', 'X1': 'X'}, [('M1.a', 'X1.a')])
                  for _ in range(3)]
    output_file = tmp_path / 'assemblies.yml'

    save_assemblies(assemblies, output_file, show_progress=False)

    # No output should be printed
    captured = capsys.readouterr()
    assert captured.out == ''


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
