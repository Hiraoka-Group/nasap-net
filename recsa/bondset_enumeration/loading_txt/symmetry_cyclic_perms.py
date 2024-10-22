import re
from collections.abc import Iterable, Sequence

from recsa import RecsaParsingError, RecsaValueError

from ...utils.cyclic_perm import cyclic_perm_to_map
from ..validation import validate_symmetry_op_name
from ..validation.perms import (check_each_bond_in_perms_once,
                                check_no_unknown_bonds_in_perms)

__all__ = ['parse_symmetry_cyclic_perms']


def parse_symmetry_cyclic_perms(
        lines: Sequence[str], bond_ids: Iterable[str]
        ) -> dict[str, dict[str, str]]:
    # Duplicate bond names are silently ignored.
    bond_ids = set(bond_ids)

    symmetry_ops = {}
    for line in lines:
        if ':' not in line:
            raise RecsaParsingError(
                f'Missing colon in line: "{line}"')
        if len(line.split(':')) > 2:
            raise RecsaParsingError(
                f'Multiple colons in line: "{line}"')

        key, value = line.split(':')
        op = key.strip()

        value = value.strip(', ')

        try:
            validate_symmetry_op_name(op)
        except RecsaValueError as e:
            raise RecsaParsingError(
                f"Error parsing symmetry operation name {op}: {e}")

        if op in symmetry_ops:
            raise RecsaParsingError(
                f'Duplicate symmetry operation name: "{op}"')

        strs_in_brackets = re.findall(r'\((.*?)\)', value)

        if not strs_in_brackets:
            raise RecsaParsingError(
                f'No permutations in line: "{line}"')

        perms = []
        for str_in_brackets in strs_in_brackets:
            perms.append([x.strip() for x in str_in_brackets.split(',')])

        check_each_bond_in_perms_once(perms, bond_ids)
        check_no_unknown_bonds_in_perms(perms, bond_ids)

        mapping = {}
        for perm in perms:
            mapping.update(cyclic_perm_to_map(perm))

        symmetry_ops[op] = mapping

        assert set(mapping.keys()) == set(bond_ids)
        assert set(mapping.values()) == set(bond_ids)

    return symmetry_ops
