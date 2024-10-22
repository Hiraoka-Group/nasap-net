import re
from collections.abc import Hashable
from typing import Any, TypeVar

from recsa import RecsaTypeError, RecsaValueError

T = TypeVar('T', bound=Hashable)

__all__ = ['validate_bond_name']


def validate_bond_name(bond: Any) -> None:
    """Validate a bond name.
    
    A bond name must be a string or an integer.
    
    - If the bond name is a string, it must consist of alphanumeric
    characters (A-Z, a-z, 0-9), underscores (_), and hyphens (-).
    - If the bond name is an integer, no further validation is performed.
    - The bond name 'None' is reserved for a bond with no adjacent bonds.

    Parameters
    ----------
    bond : Any
        A bond name.

    Raises
    ------
    RecsaTypeError
        If the bond name is neither a string nor an integer.
    RecsaValueError
        If the bond name is an empty string or 'None', or if the bond name
        is a string that does not match the regular expression pattern.
    """
    if not isinstance(bond, (str, int)):
        raise RecsaTypeError(
            f'Bond name must be a string or an integer: {bond}')
    if isinstance(bond, int):
        return
    
    # Bond name is a string.
    if not re.match(r'^[A-Za-z0-9_\-]+$', bond):
        if bond == '':
            raise RecsaValueError('Empty bond name.')
        if bond == 'None':
            # 'None' is a reserved keyword specifying that the bond
            # has no adjacent bonds.
            raise RecsaValueError(
                'Invalid bond name: "None" '
                '(reserved keyword for a bond with no adjacent bonds)')
        raise RecsaValueError(f'Invalid bond name: "{bond}"')
