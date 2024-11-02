from collections.abc import Iterable, Mapping

from .symmetry_application import apply_symmetry_operation

__all__ = ['normalize_bondset_under_sym_ops']


def normalize_bondset_under_sym_ops(
        bondset: Iterable[str],
        sym_ops: Mapping[str, Mapping[str, str]]
        ) -> set[str]:
    """Find a representative of an assembly under symmetry operations.

    There can be multiple symmetry-equivalent assemblies for a given
    assembly. This function finds the smallest one among them as a
    representative.

    # TODO: Add an example.
    """
    bondset = set(bondset)
    for sym_op in sym_ops.values():
        transformed_assem = apply_symmetry_operation(bondset, sym_op)
        if sorted(transformed_assem) < sorted(bondset):
            bondset = transformed_assem
    return bondset
