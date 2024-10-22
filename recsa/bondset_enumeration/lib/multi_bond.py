from collections.abc import Iterable, Mapping

from recsa import sort_bondsets

from .is_new_check import is_new_under_symmetry

__all__ = ['enum_multi_bond_subsets']


def enum_multi_bond_subsets(
        prev_assems: set[frozenset[str]],
        bond_to_adj_bonds: Mapping[str, Iterable[str]],
        sym_ops: Mapping[str, Mapping[str, str]] | None = None
        ) -> set[frozenset[str]]:
    """Enumerate multi-bond subsets of bonds
    excluding disconnected ones and symmetry-equivalent ones.
    """
    bond_to_adj_bonds = {
        bond: set(adj_bonds) 
        for bond, adj_bonds in bond_to_adj_bonds.items()}
    
    found: set[frozenset[str]] = set()

    # NOTE: The order of the iteration should be fixed to make the 
    # result deterministic.
    for prev in sort_bondsets(prev_assems):
        # List adjacent bonds to the bonds in the previous assembly.
        adj_bonds: set[str] = set()
        for bond in prev:
            adj_bonds.update(bond_to_adj_bonds[bond])
        # Bonds in the previous assembly should be excluded.
        adj_bonds -= prev

        # NOTE: The order of the iteration should be fixed to make 
        # the result deterministic.
        for adj_bond in sorted(adj_bonds):
            new_assem = prev | {adj_bond}
            if is_new_under_symmetry(found, new_assem, sym_ops):
                found.add(frozenset(new_assem))

    return found
