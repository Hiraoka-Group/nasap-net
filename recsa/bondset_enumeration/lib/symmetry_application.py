from collections.abc import Iterable, Mapping

__all__ = ['apply_symmetry_operation']


def apply_symmetry_operation(
        bondset: Iterable[int],
        sym_op: Mapping[int, int]
        ) -> set[int]:
    """Apply a symmetry operation to an assembly."""
    return set(sym_op[bond] for bond in bondset)
