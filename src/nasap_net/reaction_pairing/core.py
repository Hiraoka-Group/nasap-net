from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Generic

from nasap_net import Assembly, Component
from nasap_net.types import A, C, R
from ._lib import _IncorrectReactionResultError, _are_equivalent_mles, \
    _generate_sample_rev_mle
from .models import Reaction, _MLE


@dataclass(frozen=True)
class _ReactionIndex(Generic[A]):
    init_assem_id: A
    entering_assem_id: A | None
    product_assem_id: A
    leaving_assem_id: A | None


class IncorrectReactionResultError(ValueError):
    """
    Exception raised when the reproduced reaction result is inconsistent with
    the given result.
    """


def pair_reverse_reactions(
        id_to_reaction: Mapping[R, Reaction[A]],
        assemblies: Mapping[A, Assembly],
        components: Mapping[C, Component]
        ) -> dict[R, R | None]:
    """Pair reactions with their reverse reactions."""
    # TODO: 事前条件を docstring に記載（例：重複する反応なし）
    # TODO: 戻り値には全ての反応 ID を含めることを docstring に明記
    # TODO: Raise も明記

    index_to_id = defaultdict(set)
    for target_reaction_id, target_reaction in id_to_reaction.items():
        index = _ReactionIndex(
            init_assem_id=target_reaction.init_assem_id,
            entering_assem_id=target_reaction.entering_assem_id,
            product_assem_id=target_reaction.product_assem_id,
            leaving_assem_id=target_reaction.leaving_assem_id
        )
        index_to_id[index].add(target_reaction_id)

    reaction_to_reverse: dict[R, R | None] = {}

    for target_reaction_id, target_reaction in id_to_reaction.items():
        if target_reaction_id in reaction_to_reverse:
            continue

        reversed_index = _ReactionIndex(
            init_assem_id=target_reaction.product_assem_id,
            entering_assem_id=target_reaction.leaving_assem_id,
            product_assem_id=target_reaction.init_assem_id,
            leaving_assem_id=target_reaction.entering_assem_id
            )

        # Necessary condition: existence of reaction with reversed index
        candidate_ids = index_to_id.get(reversed_index)
        if not candidate_ids:
            continue

        # MLE of one of the reverse reactions.
        try:
            sample_rev_mle = _generate_sample_rev_mle(
                target_reaction, assemblies, components)
        except _IncorrectReactionResultError:
            raise IncorrectReactionResultError() from None

        # Any reaction with MLE equivalent to the sample_rev_mle
        # is a reverse reaction.
        for candidate_id in candidate_ids:
            candidate = id_to_reaction[candidate_id]
            candidate_mle = _MLE(
                candidate.metal_bs, candidate.leaving_bs,
                candidate.entering_bs)

            rev_init_assembly = assemblies[target_reaction.product_assem_id]
            rev_entering_assembly = None
            if target_reaction.leaving_assem_id is not None:
                rev_entering_assembly = assemblies[
                    target_reaction.leaving_assem_id]

            if _are_equivalent_mles(
                    rev_init_assembly, rev_entering_assembly,
                    sample_rev_mle, candidate_mle,
                    components
                    ):
                # Found the reverse reaction
                reaction_to_reverse[target_reaction_id] = candidate_id
                reaction_to_reverse[candidate_id] = target_reaction_id
                # Multiple matches are impossible since there are no
                # duplicate reactions.
                break
        else:
            reaction_to_reverse[target_reaction_id] = None

    return reaction_to_reverse
