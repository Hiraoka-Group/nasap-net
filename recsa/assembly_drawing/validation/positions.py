from recsa import RecsaParsingError

__all__ = ['validate_positions']


def validate_positions(positions: dict[str, tuple[float, ...]]) -> None:
    # Tuples should all have the same length, 2 or 3
    if not positions:
        raise RecsaParsingError('No positions found.')
    lengths = set(len(pos) for pos in positions.values())
    if len(lengths) != 1:
        raise RecsaParsingError('Positions have different lengths.')
    for length in lengths:
        if length not in {2, 3}:
            raise RecsaParsingError('Positions should be given as (x, y) or (x, y, z).')

    # Values should be tuples of floats or ints
    for position in positions.values():
        for coord in position:
            if not isinstance(coord, (float, int)):
                raise RecsaParsingError('Positions should be given as floats or ints.')
