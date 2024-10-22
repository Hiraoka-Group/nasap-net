from itertools import count
from pathlib import Path

__all__ = ['find_unique_filepath']


def find_unique_filepath(path: str | Path) -> Path:
    """Get a name that does not conflict with existing files."""
    path_obj = Path(path)
    it = count()
    while path_obj.exists():
        path_obj = path_obj.with_name(
            f'{path_obj.stem}({next(it)}){path_obj.suffix}')
    return path_obj
