from collections.abc import Hashable, Mapping
from typing import Generic, TypeVar

from recsa import RecsaValueError

__all__ = ['RecsaMapCyclicInconsistencyError']


T = TypeVar('T', bound=Hashable)


class RecsaMapCyclicInconsistencyError(Generic[T], RecsaValueError):
    """Raised when symmetry operations by map and by cyclic permutations
    are inconsistent."""

    def __init__(
            self, ops_by_map: Mapping[
                str, Mapping[T, T]],
            ops_by_perms: Mapping[str, Mapping[T, T]],
            message: str | None = None):
        self.ops_by_map: Mapping[
            str, Mapping[T, T]] = ops_by_map
        self.ops_by_perms: Mapping[
            str, Mapping[T, T]] = ops_by_perms
        super().__init__(
            message or (
                'Symmetry operations by map and by cyclic permutations '
                'are inconsistent.'))
