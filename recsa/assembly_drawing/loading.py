from pathlib import Path

import yaml

__all__ = ['load_drawing_args']


def load_drawing_args(filepath: str | Path) -> dict:
    filepath = Path(filepath)
    with filepath.open() as f:
        return yaml.safe_load(f)
