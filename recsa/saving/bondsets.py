from collections.abc import Iterable
from pathlib import Path
from typing import NewType

import yaml

from recsa.utils import find_unique_filepath

from .representers import BondSets, add_bondsets_representer

__all__ = ['save_bondsets']

add_bondsets_representer()


def save_bondsets(
        bondsets: Iterable[Iterable[str]],
        output_path: str | Path,
        *,
        overwrite: bool = False) -> None:
    """Save bondsets to a YAML file."""
    output_path = Path(output_path)

    if output_path.exists() and not output_path.is_file():
        raise ValueError('Output path should be a file path.')

    if output_path.exists() and not overwrite:
        output_path = find_unique_filepath(output_path)
        assert not output_path.exists()

    output_path.parent.mkdir(parents=True, exist_ok=True)

    bondsets_obj = BondSets(
        {frozenset(bondset) for bondset in bondsets})

    with output_path.open('w') as f:
        yaml.dump(bondsets_obj, f, default_flow_style=None)
        print(f'Saved! ---> "{output_path}"')
