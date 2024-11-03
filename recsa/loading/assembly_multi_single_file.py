from collections.abc import Iterator
from pathlib import Path
from typing import TypedDict

from recsa import Assembly

from .lib import convert_data_to_assembly
from .yaml_safe_load_all import load_yaml_all_safely

__all__ = ['load_assemblies_in_single_file']


class MappingWithAssemblyKey(TypedDict):
    """Mapping with an 'assembly' key that contains an Assembly."""
    assembly: Assembly


def load_assemblies_in_single_file(
        filepath: str | Path
        ) -> Iterator[MappingWithAssemblyKey]:
    """Load assemblies from a single YAML file.
    
    Each document in the file must contain an 'assembly' key, whose 
    value is a dictionary with the following keys:
    - 'name': NotRequired[str]
    - 'comp_id_to_kind': Mapping[str, str]
    - 'bonds': NotRequired[Iterable[Iterable[str]] | None]

    Any other keys can be included in the document, and they will be
    included in the yielded mapping.

    Parameters
    ----------
    filepath : str | Path
        Path to the file.

    Yields
    ------
    MappingWithAssemblyKey
        Mapping with an 'assembly' key that contains an Assembly.
        It contains other keys and values from the document, if any.
    """
    for data in load_yaml_all_safely(filepath):
        # Expected data format:
        # {
        #     'assembly': {
        #         'name': 'MX',  # Optional
        #         'comp_id_to_kind': {'M1': 'M', 'X1': 'X'},
        #         'bonds': [['M1.a', 'X1.a']]  # Optional
        #     },
        #     'foo': ...  # Optional
        #     ...
        # }
        data['assembly'] = convert_data_to_assembly(data['assembly'])
        yield data
