from collections.abc import Mapping
from typing import Literal, TypeAlias

from recsa import (BindsiteIdConverter, Component, InterReactionEmbedded,
                   IntraReactionEmbedded)

from .bindsite_num import get_connected_num

ReactionEmbedded: TypeAlias = (
    IntraReactionEmbedded | InterReactionEmbedded)


def calc_nth_site_on_metal(
        reaction: ReactionEmbedded,
        comp_kind_to_obj: Mapping[str, Component],
        leave_enter_order: Literal['leaving_first', 'entering_first']
        ) -> int:
    """Calculate the nth site on the metal that the entering component binds.
    
    Parameters
    ----------
    reaction : ReactionEmbedded
        The reaction object.
    comp_kind_to_obj : Mapping[str, Component]
        A mapping from component kind to component object.
    leave_enter_order : Literal['leaving_first', 'entering_first']
        The order of leaving and entering components.
        'leaving_first' means the leaving component leaves before the entering component enters, like SN1 reaction. 
        (e.g., MLX + L -> ML + X + L (transition state) -> ML2 + X)
        'entering_first' means the entering component enters before the leaving component leaves, like SN2 reaction.
        (e.g., MLX + L -> ML2X (transition state) -> ML2 + X)
    """
    already_connected_num = calc_num_of_already_connected_entering_kind(
        reaction, comp_kind_to_obj)

    if leave_enter_order == 'leaving_first':
        return _when_leaving_first(
            already_connected_num, 
            reaction.leaving_kind, reaction.entering_kind)
    elif leave_enter_order == 'entering_first':
        return _when_entering_first(
            already_connected_num, 
            reaction.leaving_kind, reaction.entering_kind)
    else:
        raise ValueError(f'Invalid order: {leave_enter_order}')


def calc_num_of_already_connected_entering_kind(
        reaction: ReactionEmbedded,
        comp_kind_to_obj: Mapping[str, Component]
        ) -> int:
    id_converter = BindsiteIdConverter()
    metal_comp_id, _ = id_converter.global_to_local(reaction.metal_bs)
    return get_connected_num(
        reaction.init_assem, metal_comp_id, reaction.entering_kind,
        comp_kind_to_obj[reaction.metal_kind])


def _when_leaving_first(
        already_connected_num: int,
        leaving_kind: str, entering_kind: str,
        ) -> int:
    if leaving_kind == entering_kind:
        # e.g., MLX + L -> MX + L + L (transition state) -> MLX + L
        # L enters the 1st site on M of ML
        return already_connected_num
    else:
        # e.g., MLX + L -> ML + X + L (transition state) -> ML2 + X
        # L enters the 2nd site on M of ML
        return already_connected_num + 1


def _when_entering_first(
        already_connected_num: int,
        leaving_kind: str, entering_kind: str,
        ) -> int:
    if leaving_kind == entering_kind:
        # e.g., MLX + L -> ML2X (transition state) -> MLX + L
        # L enters the 2nd site on M of ML
        return already_connected_num + 1
    else:
        # e.g., MLX + L -> ML2X (transition state) -> ML2 + X
        # L enters the 1st site on M of ML
        return already_connected_num + 1
