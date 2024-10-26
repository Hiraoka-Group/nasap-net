from collections.abc import Iterator
from pathlib import Path
from typing import Any

import yaml

import recsa as rx


def load_yaml_all_safely(file_path: str | Path) -> Iterator[Any]:
    file_path = Path(file_path)
    with file_path.open('r') as f:
        try:
            data = yaml.safe_load_all(f)
        except yaml.YAMLError as e:
            raise rx.RecsaLoadingError(
                f'Invalid YAML file: {file_path}') from e
        yield from data
