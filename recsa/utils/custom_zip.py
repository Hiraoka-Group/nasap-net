from collections.abc import Iterable, Iterator
from itertools import zip_longest

from recsa import RecsaValueError

__all__ = ['zip_specified_shortest']


def zip_specified_shortest(shorter: Iterable, longer: Iterable) -> Iterator:
    """Zip two iterables, raising an error if the length of 'longer' is less.

    The length of the output is equal to the length of 'shorter'.
    """
    # The reason for not using 'len(names)' and 'len(assemblies)' is to
    # keep lazy evaluation in case 'names' and 'assemblies' are generators.

    # We cannot use a string or None as 'fillvalue' because
    # they may be contained in 'names'. Using 'object()' and 'is' 
    # comparison is safer.
    obj = object()

    # 'zip_longest' fills the shorter iterable with 'fillvalue'.
    for short, long in zip_longest(shorter, longer, fillvalue=obj):
        if long is obj:
            raise RecsaValueError(
                'The length of "longer" should be equal to or greater than '
                'the length of "shorter".')
        if short is obj:
            return
        yield short, long
