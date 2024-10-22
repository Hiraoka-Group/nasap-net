from collections.abc import Mapping

from .symmetry_application import apply_symmetry_operation

__all__ = ['find_representative_under_sym_ops']


def find_representative_under_sym_ops(
        assembly: set[str],
        sym_ops: Mapping[str, Mapping[str, str]]
        ) -> set[str]:
    """Find a representative of an assembly under symmetry operations.

    There can be multiple symmetry-equivalent assemblies for a given
    assembly. This function finds the smallest one among them as a
    representative.

    # TODO: Add an example.
    """
    for sym_op in sym_ops.values():
        transformed_assem = apply_symmetry_operation(assembly, sym_op)
        if transformed_assem < assembly:
            return transformed_assem
    return assembly
