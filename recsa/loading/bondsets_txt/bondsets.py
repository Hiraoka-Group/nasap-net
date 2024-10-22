from collections.abc import Iterator
from pathlib import Path

__all__ = ['load_bondsets']


def load_bondsets(filepath: str) -> Iterator[frozenset[str]]:
    """Parse assemblies represented as lists of bonds."""
    filepath_obj = Path(filepath)
    for line in filepath_obj.open():
        line = line.strip()
        if not line:
            continue
        if line.startswith('#'):
            continue
        yield frozenset([
            x.strip() for x in line.split(',') if x.strip()])
