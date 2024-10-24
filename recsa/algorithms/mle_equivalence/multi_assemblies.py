from collections.abc import Iterable, Mapping
from typing import TypeAlias

from recsa import Assembly, Component, MleBindsite, MleKind
from recsa.algorithms.mle_equivalence.as_uf import \
    compute_mle_equivalence_as_uf
from recsa.algorithms.mle_equivalence.typing import (AssemblyId, MleToRoot,
                                                     RootToMles)

__all__ = ['compute_mle_to_root_maps']


def compute_mle_to_root_maps(
        id_to_assembly: Mapping[str, Assembly],
        mle_kinds: Iterable[MleKind],
        component_structures: Mapping[str, Component],
        ) -> dict[tuple[AssemblyId, MleKind], MleToRoot]:
    """Compute a mapping from "triple bindsites" to its root "triple bindsites".

    A "triple bindsite" is a TripleBindsite object that represents a
    metal, leaving, and entering bindsite. The root "triple bindsite" is the
    smallest "triple bindsite" in the equivalent "triple bindsite" group.
    """
    d: dict[tuple[AssemblyId, MleKind], MleToRoot] = {}
    for id_, assembly in id_to_assembly.items():
        mle_kind_to_uf = compute_mle_equivalence_as_uf(
            assembly, mle_kinds, component_structures)
        for mle_kind, uf in mle_kind_to_uf.items():
            mle_bindsite_to_root = {}
            for group in uf.to_sets():
                root = min(group)
                for mle_bindsite in group:
                    mle_bindsite_to_root[mle_bindsite] = root
            d[(id_, mle_kind)] = mle_bindsite_to_root
    return d
