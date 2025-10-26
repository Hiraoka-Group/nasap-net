from collections import defaultdict, deque
from collections.abc import Hashable, Iterable, Mapping
from typing import Any

from nasap_net.models import Assembly
from nasap_net.types import ID
from .conversion import fragment_to_assembly
from .lib import get_key, get_unique_starting_fragments, grow_fragment, is_new, \
    validate_symmetry_operation
from .models import Fragment


def enumerate_fragments(
        template: Assembly,
        symmetry_operations: Iterable[Mapping[Any, ID]] | None = None
) -> set[Assembly]:
    template_fragment = Fragment.from_assembly(template)
    if symmetry_operations is not None:
        for sym_op in symmetry_operations:
            validate_symmetry_operation(template_fragment, sym_op)

    found: defaultdict[Hashable, set[Fragment]] = defaultdict(set)

    starting_fragments = set(get_unique_starting_fragments(
        template_fragment, symmetry_operations)
    )
    for frag in starting_fragments:
        found[get_key(frag)].add(frag)
    queue = deque(sorted(starting_fragments))

    while queue:
        cur_frag = queue.popleft()
        one_step_grown_frags = grow_fragment(cur_frag, template_fragment)
        for frag in one_step_grown_frags:
            if is_new(frag, found, symmetry_operations):
                found[get_key(frag)].add(frag)
                queue.append(frag)

    result: set[Assembly] = set()
    for frags in found.values():
        result.update(fragment_to_assembly(frag, template) for frag in frags)
    return result
