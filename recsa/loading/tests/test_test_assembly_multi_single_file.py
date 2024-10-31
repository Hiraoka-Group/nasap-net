from collections.abc import Iterable
from typing import Any

import pytest
import yaml

from recsa import Assembly, assembly_equality, load_assemblies_in_single_file


# Helper function
def write_safe_data_to_file(tmp_path, data: Iterable[Any]):
    file = tmp_path / 'assemblies.yaml'
    with file.open('w') as f:
        yaml.safe_dump_all(data, f)
    return file


def test_typical_case(tmp_path):
    data = [
        {'id': 'MX2',
         'comp_id_to_kind': {'M1': 'M', 'X1': 'X', 'X2': 'X'},
         'bonds': [['M1.a', 'X1.a'], ['M1.b', 'X2.a']]},
        {'id': 'L', 'comp_id_to_kind': {'L1': 'L'}}
    ]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    
    loaded = load_assemblies_in_single_file(assemblies_file)

    assert list(loaded) == [
        ('MX2', Assembly(
            comp_id_to_kind={'M1': 'M', 'X1': 'X', 'X2': 'X'},
            bonds=[('M1.a', 'X1.a'), ('M1.b', 'X2.a')])),
        ('L', Assembly(comp_id_to_kind={'L1': 'L'}, bonds=[]))
    ]


def test_basic(tmp_path):
    data = [{'comp_id_to_kind': {'M1': 'M'}}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [
        (None, Assembly(comp_id_to_kind={'M1': 'M'}, bonds=[]))]


def test_id(tmp_path):
    data = [{'id': 'freeM', 'comp_id_to_kind': {'M1': 'M'}}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [
        ('freeM', Assembly(comp_id_to_kind={'M1': 'M'}, bonds=[]))]


def test_without_comp_id_to_kind(tmp_path):
    data = [{}]  # type: ignore
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [(None, Assembly(comp_id_to_kind={}, bonds=[]))]


def test_empty_comp_id_to_kind(tmp_path):
    data = [{'comp_id_to_kind': {}}]  # type: ignore
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [(None, Assembly(comp_id_to_kind={}, bonds=[]))]


def test_without_bonds(tmp_path):
    data = [{'comp_id_to_kind': {'M1': 'M'}}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [
        (None, Assembly(comp_id_to_kind={'M1': 'M'}, bonds=[]))]


def test_empty_bonds(tmp_path):
    data = [{'comp_id_to_kind': {'M1': 'M'}, 'bonds': []}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [
        (None, Assembly(comp_id_to_kind={'M1': 'M'}, bonds=[]))]


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
