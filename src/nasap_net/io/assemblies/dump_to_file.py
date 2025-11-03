import os
from collections.abc import Iterable
from pathlib import Path

from nasap_net.io.assemblies.dump import dump
from nasap_net.models import Assembly


def export_assemblies_to_file(
        assemblies: Iterable[Assembly],
        file_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        verbose: bool = True,
        ) -> None:
    """Dump assemblies and components into a YAML file.

    Parameters
    ----------
    assemblies : Iterable[Assembly]
        Assemblies to dump.
    file_path : os.PathLike | str
        Path to the YAML file to write.
    overwrite : bool, optional
        If True, overwrite the file if it already exists.
        If False, raise an error if the file already exists.
        Default is False.
    verbose : bool, optional
        If True, print a message indicating the file path written to.
        Default is True.
    """
    file_path = Path(file_path)
    if file_path.exists() and not overwrite:
        raise FileExistsError(
            f'File "{str(file_path)}" already exists. '
            'Use `overwrite=True` to overwrite it.'
        )

    file_path.parent.mkdir(parents=True, exist_ok=True)
    yaml_str = dump(assemblies)
    file_path.write_text(yaml_str, encoding="utf-8")
    if verbose:
        print(f'Saved! --> "{str(file_path)}"')
