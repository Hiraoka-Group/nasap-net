from collections.abc import Hashable, Iterable
from typing import Generic, TypeVar, overload

import recsa as rx

__all__ = ['FrozenUnorderedPair']


T = TypeVar('T', bound=Hashable)


class FrozenUnorderedPair(Generic[T]):
    """A frozen unordered pair of two hashable elements."""
    @overload
    def __init__(self, first: T, second: T) -> None: ...
    @overload
    def __init__(self, pair: Iterable[T]) -> None: ...
    def __init__(self, *args):
        # TODO: Add type validation.
        if len(args) == 1:
            pair = tuple(args[0])
            if len(pair) != 2:
                raise rx.RecsaValueError('The pair should have two elements.')
            self.__pair = pair
        elif len(args) == 2:
            self.__pair = tuple(args)
        else:
            raise rx.RecsaValueError('The pair should have two elements.')
    
    @property
    def first(self) -> T:
        return self.__pair[0]
    
    @property
    def second(self) -> T:
        return self.__pair[1]
    
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, FrozenUnorderedPair):
            return False
        return set(self.__pair) == set(other.__pair)
    
    def __hash__(self) -> int:
        return hash(frozenset(self.__pair))
    
    def __repr__(self) -> str:
        return f'FrozenUnorderedPair({self.__pair})'
    
    def __iter__(self):
        return iter(self.__pair)
