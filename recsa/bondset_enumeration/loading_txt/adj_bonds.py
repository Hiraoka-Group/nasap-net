from collections.abc import Iterable, Sequence

from recsa import RecsaParsingError

__all__ = ['parse_adj_bonds']


def parse_adj_bonds(
        lines: Sequence[str], bond_ids: Iterable[str]
        ) -> dict[str, set[str]]:
    bond_ids = set(bond_ids)
    bond_to_adj_bonds: dict[str, set[str]] = {}

    for line in lines:
        if ':' not in line:
            raise RecsaParsingError(f'Missing colon in line: "{line}"')
        if len(line.split(':')) > 2:
            raise RecsaParsingError(f'Multiple colons in line: "{line}"')

        key, value = line.split(':')
        bond_id = key.strip()

        if bond_id not in bond_ids:
            raise RecsaParsingError(
                f'Unknown bond name in [adj] section: "{bond_id}"')
        if bond_id in bond_to_adj_bonds:
            raise RecsaParsingError(
                f'Duplicate bond name in [adj] section: "{bond_id}"')

        # Remove leading and trailing whitespaces and commas.
        value = value.strip(', ')
        # Duplicate adjacent bond names are silently ignored.
        adj_bonds = {x.strip() for x in value.split(',')}

        # Empty adjacency list is not allowed.
        # Bonds with no adjacent bonds also should be in the list,
        # and they should be represented as 'None'.
        # e.g.,
        #   bond1: bond3, bond4
        #   bond2: None  # OK
        #   bond3: bond1
        #   bond4: bond1
        #   bond5:  # Error
        # 
        # Consequently, the name 'None' is reserved and cannot be used
        # as a bond name.
        if not adj_bonds or adj_bonds == {''}:  # Empty adjacency list
            raise RecsaParsingError(
                f'Empty adjacency list for bond "{bond_id}" in line: "{line}"')
        if adj_bonds == {'None'}:  # Adjacency list is 'None'
            adj_bonds = set()

        for adj_bond in adj_bonds:
            if adj_bond == '':
                raise RecsaParsingError(f'Empty bond name in line: "{line}"')
            if adj_bond not in bond_ids:
                raise RecsaParsingError(
                    f'Unknown adjacent bond name in [adj] section: '
                    f'"{adj_bond}" in line: "{line}"')

        bond_to_adj_bonds[bond_id] = adj_bonds

    for bond_id in bond_ids:
        # All bonds should be in the adjacency list
        # even if they have no adjacent bonds.
        # Bonds with no adjacent bonds should be represented as 'None'.
        # e.g., bond1: None
        if bond_id not in bond_to_adj_bonds:
            raise RecsaParsingError(f'No adjacent bonds for bond "{bond_id}".')

    return bond_to_adj_bonds
