from typing import Iterable

from nasap_net.reaction_exploration_im import Assembly


class _AssemblyNotFoundError(Exception):
    pass


def find_isomorphic_assembly(
        target: Assembly,
        search_space: Iterable[Assembly]
        ) -> Assembly:
    raise NotImplementedError()
