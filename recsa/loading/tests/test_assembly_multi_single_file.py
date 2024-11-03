from collections.abc import Iterable
from typing import Any

import pytest
import yaml

from recsa import Assembly, load_assemblies_in_single_file


# Helper function
def write_safe_data_to_file(tmp_path, data: Iterable[Any]):
    file = tmp_path / 'assemblies.yaml'
    with file.open('w') as f:
        yaml.safe_dump_all(data, f)
    return file


def test_typical_case(tmp_path):
    data = [
        {'index': 0,
         'assembly': {
            'name': 'MX2',
            'comp_id_to_kind': {'M1': 'M', 'X1': 'X', 'X2': 'X'},
            'bonds': [['M1.a', 'X1.a'], ['M1.b', 'X2.a']]}},
        {'index': 1, 'assembly': {'comp_id_to_kind': {'L1': 'L'}}}
    ]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    
    loaded = load_assemblies_in_single_file(assemblies_file)

    assert list(loaded) == [
        {'index': 0,
         'assembly': Assembly(
            comp_id_to_kind={'M1': 'M', 'X1': 'X', 'X2': 'X'},
            bonds=[('M1.a', 'X1.a'), ('M1.b', 'X2.a')],
            name='MX2')},
        {'index': 1, 'assembly': Assembly(comp_id_to_kind={'L1': 'L'})}
    ]


def test_basic(tmp_path):
    data = [{'assembly': {'comp_id_to_kind': {'M1': 'M'}}}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [
        {'assembly': Assembly(comp_id_to_kind={'M1': 'M'})}]


def test_missing_assembly_key(tmp_path):
    data = [{'foo': 'bar'}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    with pytest.raises(KeyError):
        list(load_assemblies_in_single_file(assemblies_file))


def test_all_args(tmp_path):
    data = [{'assembly': {
        'name': 'MX', 'comp_id_to_kind': {'M1': 'M', 'X1': 'X'},
        'bonds': [['M1.a', 'X1.a']]}}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [
        {'assembly': Assembly(
            comp_id_to_kind={'M1': 'M', 'X1': 'X'},
            bonds=[('M1.a', 'X1.a')],
            name='MX')}]


def test_other_keys(tmp_path):
    data = [{'assembly': {'comp_id_to_kind': {'M1': 'M'}},
             'foo': 'bar'}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [
        {'assembly': Assembly(comp_id_to_kind={'M1': 'M'}), 'foo': 'bar'}]


def test_name(tmp_path):
    data = [{'assembly': {'name': 'freeX', 'comp_id_to_kind': {'X1': 'X'}}}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    loaded = load_assemblies_in_single_file(assemblies_file)
    assert list(loaded) == [
        {'assembly': Assembly(comp_id_to_kind={'X1': 'X'}, name='freeX')}]


def test_without_comp_id_to_kind(tmp_path):
    data = [{'assembly': None}]
    assemblies_file = write_safe_data_to_file(tmp_path, data)
    with pytest.raises(TypeError):
        list(load_assemblies_in_single_file(assemblies_file))


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
