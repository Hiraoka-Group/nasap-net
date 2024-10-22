from pathlib import Path

import yaml

from recsa import Assembly
from recsa.utils import find_unique_filepath

from .representers import add_assembly_representer

__all__ = ['save_assembly']


add_assembly_representer()


def save_assembly(
        assembly: Assembly,
        output_path: str | Path,
        *,
        overwrite: bool = False) -> None:
    """Save an assembly as a YAML file."""
    output_path = Path(output_path)

    if output_path.exists() and not output_path.is_file():
        raise ValueError('Output path should be a file path.')

    if output_path.exists() and not overwrite:
        output_path = find_unique_filepath(output_path)
        assert not output_path.exists()

    with output_path.open('w') as f:
        yaml.dump(assembly, f, default_flow_style=None)
        print(f'Saved! ---> "{output_path}"')
