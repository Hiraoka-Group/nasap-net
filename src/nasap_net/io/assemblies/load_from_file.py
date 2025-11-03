import os
from pathlib import Path

from nasap_net.io.assemblies.load import load
from nasap_net.models import Assembly


def import_assemblies_from_file(
        file_path: os.PathLike | str,
        *,
        strict: bool = True,
        verbose: bool = True,
) -> list[Assembly]:
    """Load assemblies and components from a YAML file.

    Parameters
    ----------
    file_path : os.PathLike | str
        Path to the YAML file to load.
    strict : bool, optional
        If True, raise an error if the file does not exist.
        If False, return an empty list if the file does not exist.
        Default is True.
    verbose : bool, optional
        If True, print a message indicating the number of assemblies loaded.
        Default is True.

    Returns
    -------
    list[Assembly]
        List of loaded assemblies.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        if strict:
            raise FileNotFoundError(f'File "{str(file_path)}" does not exist.')
        return []

    yaml_str = file_path.read_text(encoding="utf-8")
    assemblies = load(yaml_str)
    if verbose:
        print(f'Loaded {len(assemblies)} assemblies from "{str(file_path)}"')
    return assemblies
