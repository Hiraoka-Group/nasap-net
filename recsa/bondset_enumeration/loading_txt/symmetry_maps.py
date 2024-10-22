from collections.abc import Iterable, Sequence

from recsa import RecsaParsingError, RecsaValueError

from ..validation import validate_symmetry_op_name

__all__ = ['parse_symmetry_maps']


def parse_symmetry_maps(
        lines: Sequence[str], bond_ids: Iterable[str]
        ) -> dict[str, dict[str, str]]:
    # Duplicate bond names are silently ignored.
    bond_ids = set(bond_ids)

    symmetry_ops: dict[str, dict[str, str]] = {}

    for line in lines:
        if ':' not in line:
            raise RecsaParsingError(f'Missing colon in line: "{line}"')
        if len(line.split(':')) > 2:
            raise RecsaParsingError(f'Multiple colons in line: "{line}"')

        key, value = line.split(':')
        op = key.strip()

        try:
            validate_symmetry_op_name(op)
        except RecsaValueError as e:
            raise RecsaParsingError(
                f"Error parsing symmetry operation name {op}: {e}")

        if op in symmetry_ops:
            raise RecsaParsingError(
                f'Duplicate symmetry operation name: "{op}"')

        # Remove leading and trailing commas and whitespaces.
        value = value.strip(', ')

        mapping: dict[str, str] = {}
        for map_str in value.split(','):
            if '->' not in map_str:
                raise RecsaParsingError(f'Missing "->" in line: "{line}"')
            if len(map_str.split('->')) > 2:
                raise RecsaParsingError(
                    f'Multiple "->" in one mapping in line: "{line}"')

            source, target = map_str.split('->')
            source, target = source.strip(), target.strip()
            mapping[source] = target

            if source not in bond_ids:
                raise RecsaParsingError(
                    f'Unknown source bond name "{source}" in line: "{line}"')
            if target not in bond_ids:
                raise RecsaParsingError(
                    f'Unknown target bond name "{target}" in line: "{line}"')

        for bond in bond_ids:
            if bond not in mapping.keys():
                raise RecsaParsingError(
                    f'Mapping for bond "{bond}" is missing.')

        for bond in bond_ids:
            if bond not in mapping.values():
                raise RecsaParsingError(
                    f'No bond maps to "{bond}".')

        symmetry_ops[op] = mapping

    return symmetry_ops
