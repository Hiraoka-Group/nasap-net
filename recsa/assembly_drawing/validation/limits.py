from recsa import RecsaParsingError

__all__ = ['validate_limits']


def validate_limits(limits: dict[str, tuple[float, ...]]) -> None:
    # keys should be 'x', 'y', or 'z'
    if not limits:
        raise RecsaParsingError('No limits found.')
    AXES_2D = {'x', 'y'}
    AXES_3D = {'x', 'y', 'z'}
    if set(limits.keys()) not in (AXES_2D, AXES_3D):
        raise RecsaParsingError('Limits should be given for x, y, and z axes.')

    # values should be tuples of length 2: (min, max)
    for limit in limits.values():
        if len(limit) != 2:
            raise RecsaParsingError('Limits should be given as (min, max).')

        if limit[0] >= limit[1]:
            raise RecsaParsingError('Minimum should be less than maximum.')
