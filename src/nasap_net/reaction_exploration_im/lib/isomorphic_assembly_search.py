from typing import Iterable

from nasap_net.models import Assembly


class _AssemblyNotFoundError(Exception):
    pass


def find_isomorphic_assembly(
        target: Assembly,
        search_space: Iterable[Assembly]
        ) -> Assembly:
    raise NotImplementedError()
