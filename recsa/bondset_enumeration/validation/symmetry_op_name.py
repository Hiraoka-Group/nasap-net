import re
from typing import Any

from recsa import RecsaTypeError, RecsaValueError

__all__ = ['validate_symmetry_op_name']


def validate_symmetry_op_name(op: Any) -> None:
    """Validate a symmetry operation name.

    A symmetry operation name must be a string or an integer.

    - If the symmetry operation name is a string, it must consist of
    alphanumeric characters, underscores, hyphens, and parentheses.
    - If the symmetry operation name is an integer, no further validation
    is performed.

    Parameters
    ----------
    op : Any
        A symmetry operation name.

    Raises
    ------
    RecsaTypeError
        If the symmetry operation name is neither a string nor an integer.
    RecsaValueError
        If the symmetry operation name is an empty string, or if the
        symmetry operation name is a string that does not match the
        regular expression pattern.
    """
    if not isinstance(op, (str, int)):
        raise RecsaTypeError(
            f'Symmetry operation name must be a string or an integer: {op}')
    if isinstance(op, int):
        return

    # Symmetry operation name is a string.
    if not re.match(r'^[A-Za-z0-9_\-^()]+$', op):
        if op == '':
            raise RecsaValueError('Empty symmetry operation name.')
        raise RecsaValueError(
            f'Invalid symmetry operation name: "{op}"')
