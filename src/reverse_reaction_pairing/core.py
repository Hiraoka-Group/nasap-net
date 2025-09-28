from collections import defaultdict
from collections.abc import Mapping
from dataclasses import dataclass
from typing import Generic, TypeVar

from nasap_net import Assembly, Component
from .lib import _MLE, _are_equivalent_mles, \
    _determine_right_hand_side_mle

_A = TypeVar("_A", int, str)  # Assembly ID
_C = TypeVar('_C', int, str)  # Component ID
_R = TypeVar('_R', int, str)  # Reaction ID


@dataclass(frozen=True)
class Reaction(Generic[_A]):
    init_assem_id: _A
    entering_assem_id: _A | None
    product_assem_id: _A
    leaving_assem_id: _A | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int


@dataclass(frozen=True)
class ReactionIndex(Generic[_A]):
    init_assem_id: _A
    entering_assem_id: _A | None
    product_assem_id: _A
    leaving_assem_id: _A | None


def pair_reverse_reactions(
        id_to_reactions: Mapping[_R, Reaction[_A]],
        assemblies: Mapping[_A, Assembly],
        components: Mapping[_C, Component]
        ) -> dict[_R, _R | None]:
    """Pair reactions with their reverse reactions."""
    # TODO: 事前条件を docstring に記載（例：重複する反応なし）
    # TODO: 戻り値には全ての反応 ID を含めることを docstring に明記

    index_to_id = defaultdict(set)
    for rid, reaction in id_to_reactions.items():
        index = ReactionIndex(
            init_assem_id=reaction.init_assem_id,
            entering_assem_id=reaction.entering_assem_id,
            product_assem_id=reaction.product_assem_id,
            leaving_assem_id=reaction.leaving_assem_id
        )
        index_to_id[index].add(rid)

    reaction_to_reverse: dict[_R, _R | None] = {}

    for rid, reaction in id_to_reactions.items():
        reversed_index = ReactionIndex(
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
