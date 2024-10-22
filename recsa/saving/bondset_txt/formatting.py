from collections.abc import Iterator

from recsa import sort_bondsets

__all__ = ['format_bond_subsets']


def format_bond_subsets(
        bond_subsets: set[frozenset[str]]
        ) -> Iterator[str]:
    """Format the results of `enum_bond_subsets` for saving to a file.
    """
    for assem in sort_bondsets(bond_subsets):
        yield ', '.join(str(bond) for bond in sorted(assem))
