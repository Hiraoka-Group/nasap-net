from collections.abc import Iterator
from pathlib import Path
from typing import Any

from pydantic import BaseModel, field_validator

import recsa as rx
from recsa.loading.yaml_safe_load import load_yaml_safely


def load_bondsets(file_path: str | Path) -> list[list[str]]:
    """Load bondsets from a YAML file.

    Parameters
    ----------
    file_path : str or Path
        The path to the file containing the bondsets.

    Returns
    -------
    list[list[str]]
        The bondsets.

    Raises
    ------
    RecsaLoadingError
        If the file does not contain valid bondsets.
    """
    file_path = Path(file_path)
    data = load_yaml_safely(file_path)
    try:
        bondsets = _convert_data_to_bondsets(data)
    except rx.RecsaParsingError as e:
        raise rx.RecsaLoadingError(
            f'Invalid bondsets data in {file_path}'
            ) from e
    return bondsets


def _convert_data_to_bondsets(data: Any) -> list[list[str]]:
    """Convert data to a list of bondsets.

    The data should be a list of lists of strings or integers.
    Integers will be converted to strings.

    The order of the bondsets and bonds will be preserved.
    
    Parameters
    ----------
    data : Any
        The data to convert. Should be a list of lists of strings 
        or integers.

    Returns
    -------
    list[list[str]]
        The converted data.

    Raises
    ------
    RecsaParsingError
        If the data is not a list of lists of strings
    """
    if not isinstance(data, list):
        raise rx.RecsaParsingError(
            f'Expected a list of bondsets, got {type(data)}'
        )
    for bondset in data:
        if not isinstance(bondset, list):
            raise rx.RecsaParsingError(
                f'Expected a list of bonds, got {type(bondset)}'
            )
        for bond in bondset:
            if not isinstance(bond, str) and not isinstance(bond, int):
                raise rx.RecsaParsingError(
                    f'Expected a string or integer bond, got {type(bond)}'
                )
    return [[str(bond) for bond in bondset] for bondset in data]
