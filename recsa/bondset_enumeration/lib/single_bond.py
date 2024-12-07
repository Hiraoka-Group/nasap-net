from collections.abc import Iterable, Mapping

from .is_new_check import is_new_under_symmetry

__all__ = ['enum_single_bond_subsets']


def enum_single_bond_subsets(
        bonds: Iterable[int],
        sym_ops: Mapping[str, Mapping[int, int]] | None = None
        ) -> set[frozenset[int]]:
    """Enumerate single-bond subsets of bonds 
    excluding disconnected ones and symmetry-equivalent ones.
    """
    found: set[frozenset[int]] = set()

    # NOTE: The order of the iteration should be fixed to make the
    # result deterministic.
    for bond in bonds:
        assembly = {bond}
        if is_new_under_symmetry(found, assembly, sym_ops):
            found.add(frozenset(assembly))

    return set(found)
