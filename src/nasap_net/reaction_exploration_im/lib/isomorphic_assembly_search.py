from typing import Iterable, TypeVar

from nasap_net.reaction_exploration_im import Assembly


class _AssemblyNotFoundError(Exception):
    pass


_S = TypeVar('_S', bound=Assembly)
_T = TypeVar('_T', bound=Assembly)


def find_isomorphic_assembly(
        target: _S,
        search_space: Iterable[_T]
        ) -> _T:
    raise NotImplementedError()
