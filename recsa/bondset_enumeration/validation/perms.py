from collections.abc import Iterable
from itertools import chain

from recsa import RecsaParsingError

__all__ = [
    'check_each_bond_in_perms_once',
    'check_no_unknown_bonds_in_perms',
]


def check_each_bond_in_perms_once(
        perms: Iterable[Iterable[str]],
        bonds: Iterable[str]) -> None:
    bonds = set(bonds)
    bonds_in_perms = list(chain(*perms))
    if len(bonds_in_perms) == len(set(bonds_in_perms))\
            and set(bonds_in_perms) == set(bonds):
        return

    for bond in bonds:
        if bonds_in_perms.count(bond) == 0:
            raise RecsaParsingError(
                f'Bond "{bond}" is missing in cyclic permutations.')
        if bonds_in_perms.count(bond) > 1:
            raise RecsaParsingError(
                f'Duplicate bond "{bond}" in cyclic permutations.')


def check_no_unknown_bonds_in_perms(
        perms: Iterable[Iterable[str]],
        bonds: Iterable[str]) -> None:
    bonds = set(bonds)
    for bond in chain(*perms):
        if bond not in bonds:
            raise RecsaParsingError(
                f'Unknown bond "{bond}" in cyclic permutations.')