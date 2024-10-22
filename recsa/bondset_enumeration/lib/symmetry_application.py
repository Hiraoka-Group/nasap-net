from collections.abc import Mapping

__all__ = ['apply_symmetry_operation']


def apply_symmetry_operation(
        assembly: set[str],
        sym_op: Mapping[str, str]
        ) -> set[str]:
    """Apply a symmetry operation to an assembly."""
    return set(sym_op[bond] for bond in assembly)
