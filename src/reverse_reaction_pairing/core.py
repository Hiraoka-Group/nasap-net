from collections import defaultdict
from collections.abc import Hashable, Mapping
from dataclasses import dataclass
from typing import Generic, TypeVar

from nasap_net import Assembly, Component
from .lib import _are_equivalent_reactions, _generate_reverse_reaction

_A = TypeVar("_A", int, str)  # Assembly ID
_C = TypeVar('_C', int, str)  # Component ID
_R = TypeVar('_R', int, str)  # Reaction ID
_GK = TypeVar('_GK', bound=Hashable)  # Group Key


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
        id_to_reactions: Mapping[_R, Reaction],
        assemblies: Mapping[_A, Assembly],
        components: Mapping[_C, Component]
        ) -> dict[_R, _R | None]:
    """Pair reactions with their reverse reactions."""
    # TODO: 事前条件を docstring に記載（例：重複する反応なし）

    # ID 付与
    # ある反応の逆反応を生成
    # 生成した逆反応と等価な反応をグループ内で探索
    #   見つかったら双方向に記録
    #   見つからなかったら None を記録

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
        candidate_ids = index_to_id.get(reversed_index)
        if not candidate_ids:
            continue

        sample_reverse_reaction = _generate_reverse_reaction(
            reaction, assemblies, components)

        for candidate_id in candidate_ids:
            if _are_equivalent_reactions(
                    sample_reverse_reaction, id_to_reactions[candidate_id],
                    assemblies, components
                    ):
                reaction_to_reverse[rid] = candidate_id
                reaction_to_reverse[candidate_id] = rid
                break
                # Multiple matches are impossible since there are no
                # duplicate reactions.
        else:
            reaction_to_reverse[rid] = None

    return reaction_to_reverse
