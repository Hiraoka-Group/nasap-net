from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Generic

from nasap_net import Assembly, Component
from nasap_net.types import A, C, R
from ._lib import _MLE, _are_equivalent_mles, \
    _determine_right_hand_side_mle
from .models import Reaction


@dataclass(frozen=True)
class _ReactionIndex(Generic[A]):
    init_assem_id: A
    entering_assem_id: A | None
    product_assem_id: A
    leaving_assem_id: A | None


def pair_reverse_reactions(
        id_to_reactions: Mapping[R, Reaction[A]],
        assemblies: Mapping[A, Assembly],
        components: Mapping[C, Component]
        ) -> dict[R, R | None]:
    """Pair reactions with their reverse reactions."""
    # TODO: 事前条件を docstring に記載（例：重複する反応なし）
    # TODO: 戻り値には全ての反応 ID を含めることを docstring に明記

    index_to_id = defaultdict(set)
    for rid, reaction in id_to_reactions.items():
        index = _ReactionIndex(
            init_assem_id=reaction.init_assem_id,
            entering_assem_id=reaction.entering_assem_id,
            product_assem_id=reaction.product_assem_id,
            leaving_assem_id=reaction.leaving_assem_id
        )
        index_to_id[index].add(rid)

    reaction_to_reverse: dict[R, R | None] = {}

    for rid, reaction in id_to_reactions.items():
        reversed_index = _ReactionIndex(
            init_assem_id=reaction.product_assem_id,
            entering_assem_id=reaction.leaving_assem_id,
            product_assem_id=reaction.init_assem_id,
            leaving_assem_id=reaction.entering_assem_id
            )

        # Necessary condition: existence of reaction with reversed index
        candidate_ids = index_to_id.get(reversed_index)
        if not candidate_ids:
            continue

        right_hand_side_mle = _determine_right_hand_side_mle(
            reaction, assemblies, components)

        for candidate_id in candidate_ids:
            candidate = id_to_reactions[candidate_id]
            candidate_mle = _MLE(
                candidate.metal_bs, candidate.leaving_bs, candidate.entering_bs)

            init_assembly = assemblies[reaction.init_assem_id]
            entering_assembly = None
            if reaction.entering_assem_id is not None:
                entering_assembly = assemblies[reaction.entering_assem_id]

            if _are_equivalent_mles(
                    init_assembly, entering_assembly,
                    right_hand_side_mle, candidate_mle,
                    components
                    ):
                # Found the reverse reaction
                reaction_to_reverse[rid] = candidate_id
                reaction_to_reverse[candidate_id] = rid
                # Multiple matches are impossible since there are no
                # duplicate reactions.
                break
        else:
            reaction_to_reverse[rid] = None

    return reaction_to_reverse
