import logging
from collections.abc import Iterable
from itertools import chain, product
from typing import Iterator, TypeVar

from nasap_net.exceptions import DuplicateIDError, IDNotSetError
from nasap_net.models import Assembly
from nasap_net.types import ID
from .explorer import InterReactionExplorer, IntraReactionExplorer
from .lib import ReactionOutOfScopeError, ReactionResolver
from .models import MLEKind, Reaction

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())

_T = TypeVar('_T', bound=ID)

def explore_reactions(
        assemblies: Iterable[Assembly],
        mle_kinds: Iterable[MLEKind],
        ) -> Iterator[Reaction]:
    logger.debug('Starting reaction exploration.')
    assemblies = list(assemblies)

    assembly_ids: set[ID] = set()
    # All assemblies must have IDs and unique IDs
    for assem in assemblies:
        if assem.id_or_none is None:
            raise IDNotSetError(
                'All assemblies must have IDs for reaction exploration.'
            )
        if assem.id_ in assembly_ids:
            raise DuplicateIDError(
                f'Duplicate assembly ID found: {assem.id_}'
            )
        assembly_ids.add(assem.id_)

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

    for i, reaction in enumerate(chain.from_iterable(reaction_iters)):
        try:
            resolved = resolver.resolve(reaction)
            logger.info('Reaction Found (%d): %s', i, resolved)
            yield resolved
        except ReactionOutOfScopeError:
            continue
    logger.debug('Reaction exploration completed.')
