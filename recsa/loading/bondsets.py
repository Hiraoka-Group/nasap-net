from collections.abc import Iterable, Iterator, Mapping
from pathlib import Path
from typing import Any

from pydantic import BaseModel, field_validator

import recsa as rx
from recsa.loading.yaml_safe_load import load_yaml_safely


def load_bondsets(file_path: str | Path) -> dict[int, set[str]]:
    """Load bondsets from a YAML file.

    Parameters
    ----------
    file_path : str or Path
        The path to the file containing the bondsets.

    Returns
    -------
    dict[int, set[str]]
        The bondsets loaded from the file. 
        The keys are the indices of the bondsets.

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


def _convert_data_to_bondsets(data: Any) -> dict[int, set[str]]:
    """Convert data to a list of bondsets."""
    if isinstance(data, dict):
        return _convert_dict_data_to_bondsets(data)
    if isinstance(data, list):
        return _convert_list_data_to_bondsets(data)
    raise rx.RecsaParsingError(
        f'Expected a list or dict of bondsets, got {type(data)}')


def _convert_list_data_to_bondsets(
        bondsets: Iterable[Iterable[str]]) -> dict[int, set[str]]:
    return {
        i: set(str(bond) for bond in bondset) 
        for i, bondset in enumerate(bondsets)}


def _convert_dict_data_to_bondsets(
        data: Mapping[int, Iterable[str]]) -> dict[int, set[str]]:
    return {
        i: set(str(bond) for bond in bondset)
        for i, bondset in data.items()}
