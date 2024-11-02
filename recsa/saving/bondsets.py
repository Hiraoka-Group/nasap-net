from collections.abc import Iterable
from pathlib import Path
from typing import NewType

import yaml
from yamlcore import CoreDumper

from recsa.utils import find_unique_filepath

__all__ = ['save_bondsets']


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

    formatted = sorted(
        (sorted(bondset) for bondset in bondsets),
        key=lambda x: (len(x), x))

    with output_path.open('w') as f:
        yaml.dump(
            formatted, f, default_flow_style=None,
            Dumper=CoreDumper)
        print(f'Saved! ---> "{output_path}"')
