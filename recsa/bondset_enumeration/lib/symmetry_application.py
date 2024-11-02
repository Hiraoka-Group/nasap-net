from collections.abc import Iterable, Mapping

__all__ = ['apply_symmetry_operation']


def apply_symmetry_operation(
        bondset: Iterable[str],
        sym_op: Mapping[str, str]
        ) -> set[str]:
    """Apply a symmetry operation to an assembly."""
    return set(sym_op[bond] for bond in bondset)
