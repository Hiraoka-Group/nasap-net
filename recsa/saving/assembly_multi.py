import shutil
from collections.abc import Iterable
from itertools import count
from pathlib import Path

import yaml

from recsa import Assembly, RecsaValueError
from recsa.utils import find_unique_filepath, zip_specified_shortest

from .representers import add_assembly_representer

__all__ = ['save_assemblies', ]


add_assembly_representer()


def save_assemblies(
        assemblies: Iterable[Assembly], 
        output_dir: str | Path,
        names: Iterable[str] | None = None,  # TODO: Change to name_gen: Callable[[], str] = None
        *,
        overwrite_folder: bool = False) -> None:
    """Save assemblies to a file."""
    output_dir = Path(output_dir)

    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError('Output path should be a directory path.')

    if output_dir.exists():
        if overwrite_folder:
            # Remove the existing folder together with its contents
            shutil.rmtree(output_dir)
        else:
            output_dir = find_unique_filepath(output_dir)
            assert not output_dir.exists()
    
    output_dir.mkdir(parents=True, exist_ok=True)

    if names is None:
        names = (f'{i}' for i in count())

    # Save as YAML
    for assembly, name in zip_specified_shortest(assemblies, names):
        # Raise an error if there is a name conflict
        file_path = output_dir / f'{name}.yaml'
        if file_path.exists():
            raise RecsaValueError(
                f'File "{file_path}" already exists.')
        with file_path.open('w') as f:
            yaml.dump(assembly, f, default_flow_style=None)
            print(f'Saved! ---> "{file_path}"')
