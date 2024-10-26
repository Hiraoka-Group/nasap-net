from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from typing import Any, TypeAlias

from recsa import Assembly

from .assembly import load_assembly
from .yaml_safe_load_all import load_yaml_all_safely

__all__ = ['load_assemblies_in_one_file']


def load_assemblies_in_one_file(
        filepath: str | Path
        ) -> Iterator[tuple[str, Assembly]]:
    for data in load_yaml_all_safely(filepath):
        yield data.get('id'), data_to_assembly(data)


def data_to_assembly(data: Any) -> Assembly:
    # Expected data format:
    # {
    #     'comp_id_to_kind': {'M1': 'M', 'X1': 'X', 'X2': 'X'},
    #     'bonds': [['M1.a', 'X1.a'], ['M1.b', 'X2.a']]
    # }
    if not isinstance(data, Mapping):
        raise TypeError(f"Expected a mapping, but got {type(data)}")
    
    comp_id_to_kind = data.get('comp_id_to_kind')
    validate_comp_id_to_kind(comp_id_to_kind)
        
    bonds = data.get('bonds')
    validate_bonds(bonds)
    
    return Assembly(comp_id_to_kind=comp_id_to_kind, bonds=bonds)


def validate_comp_id_to_kind(comp_id_to_kind: Any) -> None:
    if comp_id_to_kind is None:
        return
    if not isinstance(comp_id_to_kind, Mapping):
        raise TypeError(f"Expected a mapping, but got {type(comp_id_to_kind)}")
    for comp_id, kind in comp_id_to_kind.items():
        if not isinstance(comp_id, str):
            raise TypeError(f"Expected a string, but got {type(comp_id)}")
        if not isinstance(kind, str):
            raise TypeError(f"Expected a string, but got {type(kind)}")


def validate_bonds(bonds: Any) -> None:
    if bonds is None:
        return
    if not isinstance(bonds, Iterable):
        raise TypeError(f"Expected an iterable, but got {type(bonds)}")
    for bond in bonds:
        if not isinstance(bond, Iterable):
            raise TypeError(f"Expected an iterable, but got {type(bond)}")
        if len(list(bond)) != 2:
            raise ValueError(f"Expected a length of 2, but got {len((list(bond)))}")
        for bindsite in bond:
            if not isinstance(bindsite, str):
                raise TypeError(f"Expected a string, but got {type(bindsite)}")
