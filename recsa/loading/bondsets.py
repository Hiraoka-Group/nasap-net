from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml
from pydantic import BaseModel, field_validator

__all__ = ['load_bondsets']


def load_bondsets(file_path: str | Path) -> list[list[str]]:
    """Load an Assembly object from a YAML file."""
    file_path = Path(file_path)
    data = load_yaml(file_path)
    return convert_data_to_bondsets(data)


def load_yaml(file_path: str | Path) -> list[list[Any]]:
    """Load YAML file and return the data as a dictionary."""
    file_path = Path(file_path)
    with file_path.open('r') as f:
        data = yaml.safe_load(f)
    return data


def convert_data_to_bondsets(data: list[list[Any]]) -> list[list[str]]:
    return sorted(
        [sorted([str(bond) for bond in bondset]) for bondset in data],
        key=lambda x: (len(x), x)
    )
