from collections.abc import Sequence

from recsa import RecsaParsingError, RecsaTypeError, RecsaValueError

from ..validation import validate_bond_name

__all__ = ['parse_bonds']


def parse_bonds(lines: Sequence[str]) -> set[str]:
    if len(lines) == 0:
        raise RecsaParsingError('Empty [bonds] section.')
    if len(lines) > 1:
        raise RecsaParsingError('Multiple lines in [bonds] section.')

    line = lines[0]
    if not line or line.isspace():
        raise RecsaParsingError('Empty [bonds] section.')
    line = line.strip(', ')

    # Duplicate bond names are silently ignored.
    bond_ids = {x.strip() for x in line.split(',')}
    for bond_id in bond_ids:
        try:
            validate_bond_name(bond_id)
        except (RecsaTypeError, RecsaValueError) as e:
            raise RecsaParsingError(
                f"Error parsing bond_id {bond_id}: {e}")
    return bond_ids