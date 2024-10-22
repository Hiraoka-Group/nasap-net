from collections.abc import Hashable, Mapping
from typing import TypeVar

from ..exceptions import RecsaMapCyclicInconsistencyError

__all__ = ['validate_symmetry_ops_consistency']


T = TypeVar('T', bound=Hashable)


def validate_symmetry_ops_consistency(
        ops_by_map: Mapping[str, Mapping[T, T]],
        ops_by_perms: Mapping[str, Mapping[T, T]]
        ) -> None:
    """Check the consistency of symmetry operations.

    Check if the symmetry operations by map and by cyclic permutations
    are consistent.
    Note that the input dictionaries are assumed to be validated
    independently before calling this function.

    Parameters
    ----------
    ops_by_map : Mapping[SymmetryOpId, Mapping[BondId, BondId]]
        Symmetry operations by map.
        A dictionary of symmetry operations.
        Each key is the name of a symmetry operation, and its value is
        a mapping of bond IDs to their images under the symmetry operation.
    ops_by_perms : Mapping[SymmetryOpId, Mapping[BondId, BondId]]
        Symmetry operations by cyclic permutations.
        A dictionary of symmetry operations.
        Each key is the name of a symmetry operation, and its value is
        a mapping of bond IDs to their images under the symmetry operation.

    Raises
    ------
    RecsaMapCyclicInconsistencyError
        If the symmetry operations by map and by cyclic permutations
        are inconsistent.
    """
    if ops_by_map == ops_by_perms:
        return

    if ops_by_map.keys() != ops_by_perms.keys():
        extra_ops_by_map = ops_by_map.keys() - ops_by_perms.keys()
        extra_ops_by_perms = ops_by_perms.keys() - ops_by_map.keys()

        raise RecsaMapCyclicInconsistencyError(
            ops_by_map, ops_by_perms,
            f'Inconsistent symmetry operations: '
            f'Extra operations in [map]: {extra_ops_by_map}, '
            f'Extra operations in [cyclic]: {extra_ops_by_perms}')

    for op in ops_by_map:
        mapping_by_map = ops_by_map[op]
        mapping_by_perms = ops_by_perms[op]

        if mapping_by_map == mapping_by_perms:
            continue

        for source in ops_by_map[op]:
            target_by_map = mapping_by_map[source]
            target_by_perms = mapping_by_perms[source]
            if target_by_map != target_by_perms:
                raise RecsaMapCyclicInconsistencyError(
                    ops_by_map, ops_by_perms,
                    f'Inconsistent symmetry operations for operation {op}: '
                    f'Mismatched mapping for source {source}: '
                    f'by map: {target_by_map}, by cyclic: {target_by_perms}')
