import os
from collections.abc import Iterable
from pathlib import Path

from nasap_net.models import Assembly
from ..dump import dump


def dump_to_file(
        assemblies: Iterable[Assembly],
        file_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        verbose: bool = True,
        ) -> None:
    """Dump assemblies and components into a YAML file."""
    file_path = Path(file_path)
    if file_path.exists() and not overwrite:
        raise FileExistsError(
            f'File "{str(file_path)}" already exists. '
            'Use `overwrite=True` to overwrite it.'
        )

    file_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_str = dump(assemblies)
    file_path.write_text(yaml_str)
    if verbose:
        print(f'Saved! --> "{str(file_path)}"')
