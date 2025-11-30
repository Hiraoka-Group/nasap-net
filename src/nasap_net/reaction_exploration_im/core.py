import logging
from collections.abc import Iterable
from itertools import chain, product
from typing import Iterator, TypeVar

from nasap_net.helpers import validate_unique_ids
from nasap_net.models import Assembly, MLEKind, Reaction
from nasap_net.types import ID
from .explorer import InterReactionExplorer, IntraReactionExplorer
from .lib import ReactionOutOfScopeError, ReactionResolver

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_T = TypeVar('_T', bound=ID)

def explore_reactions(
        assemblies: Iterable[Assembly],
        mle_kinds: Iterable[MLEKind],
        ) -> Iterator[Reaction]:
    logger.debug('Starting reaction exploration.')
    assemblies = list(assemblies)

    validate_unique_ids(assemblies)

    reaction_iters: list[Iterator[Reaction]] = []
    for mle_kind in mle_kinds:
        # Intra-molecular reactions
        for assem in assemblies:
            intra_explorer = IntraReactionExplorer(assem, mle_kind)
            reaction_iters.append(intra_explorer.explore())

        # Inter-molecular reactions
        for init_assem, entering_assem in product(assemblies, repeat=2):
            inter_explorer = InterReactionExplorer(
                init_assem, entering_assem, mle_kind)
            reaction_iters.append(inter_explorer.explore())

    resolver = ReactionResolver(assemblies)

    counter = 0

    for reaction in chain.from_iterable(reaction_iters):
        try:
            resolved = resolver.resolve(reaction)
            logger.debug('Reaction Found (%d): %s', counter, resolved)
            counter += 1
            yield resolved
        except ReactionOutOfScopeError:
            continue
    logger.debug('Reaction exploration completed.')
