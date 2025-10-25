from collections.abc import Iterable

from nasap_net.models import Assembly, Component


def cap_fragments_with_ligand(
        fragments: Iterable[Assembly],
        *,
        leaving_ligand: Component
) -> list[Assembly]:
    raise NotImplementedError()
