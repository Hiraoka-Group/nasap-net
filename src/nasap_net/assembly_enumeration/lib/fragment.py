from collections import defaultdict, deque
from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar

from nasap_net.models import Assembly
from nasap_net.types import ID

_T = TypeVar('_T', bound=ID)

def enumerate_fragments(
        template: Assembly,
        symmetry_operations: Iterable[Mapping[_T, ID]] | None = None
) -> list[Assembly]:
    found: defaultdict[Hashable, set[Assembly]] = defaultdict(set)
    queue = deque(get_starting_fragments(template))

    while queue:
        cur_frag = queue.popleft()
        one_step_grown_frags = grow_fragment(cur_frag, template)
        for frag in one_step_grown_frags:
            if is_new(frag, found, symmetry_operations):
                found[get_key(frag)].add(frag)
                queue.append(frag)

    result: list[Assembly] = []
    for frags in found.values():
        result.extend(frags)
    return result


def get_key(assembly: Assembly) -> Hashable:
    raise NotImplementedError()


def get_starting_fragments(template: Assembly) -> Iterable[Assembly]:
    raise NotImplementedError()


def grow_fragment(
        fragment: Assembly,
        template: Assembly
) -> Iterable[Assembly]:
    raise NotImplementedError()


def is_new(
        fragment: Assembly,
        found: defaultdict[Hashable, set[Assembly]],
        symmetry_operations: Iterable[Mapping[_T, ID]] | None = None
) -> bool:
    raise NotImplementedError()
