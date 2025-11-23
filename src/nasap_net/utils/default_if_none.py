from typing import Any, TypeVar, overload

T = TypeVar('T')

@overload
def default_if_none(value: None, default: T) -> T: ...
@overload
def default_if_none(value: T, default: Any) -> T: ...
def default_if_none(value, default):
    """Return the value if it is not None, otherwise return the default."""
    return value if value is not None else default
