from collections.abc import Iterable, Mapping
from itertools import chain, product
from typing import Iterator

from nasap_net.types import ID
from .explorer import InterReactionExplorer, IntraReactionExplorer
from .lib import _ReactionOutOfScopeError, \
    _represent_reaction_with_given_assemblies
from .models import MLEKind, Reaction
from ..models import Assembly


def explore_reactions(
        assemblies: Mapping[ID, Assembly],
        mle_kinds: Iterable[MLEKind],
        ) -> Iterator[Reaction]:
    # Add assembly IDs to assemblies
    assems_with_ids = [
        assem.copy_with(id_=assem_id)
        for assem_id, assem in assemblies.items()]

    reaction_iters: list[Iterator[Reaction]] = []
    for mle_kind in mle_kinds:
        # Intra-molecular reactions
        for assem in assems_with_ids:
            intra_explorer = IntraReactionExplorer(assem, mle_kind)
            reaction_iters.append(intra_explorer.explore())

        # Inter-molecular reactions
        for init_assem, entering_assem in product(assems_with_ids, repeat=2):
            inter_explorer = InterReactionExplorer(
                init_assem, entering_assem, mle_kind)
            reaction_iters.append(inter_explorer.explore())

    for reaction in chain.from_iterable(reaction_iters):
        try:
            yield _represent_reaction_with_given_assemblies(
                reaction, assems_with_ids)
        except _ReactionOutOfScopeError:
            continue
