from typing import TypeVar

T = TypeVar("T")

def default_if_none(value: T | None, default: T) -> T:
    """Return the value if it is not None, otherwise return the default."""
    return value if value is not None else default
