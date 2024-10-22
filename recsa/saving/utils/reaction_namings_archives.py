from recsa.classes.reaction import InterReaction, IntraReaction

__all__ = ['generate_reaction_name']


def generate_reaction_name(reaction: IntraReaction | InterReaction) -> str:
    left_assems = [reaction.init_assem_id]
    if reaction.entering_assem_id is not None:
        left_assems.append(reaction.entering_assem_id)
    right_assems = [reaction.product_assem_id]
    if reaction.leaving_assem_id is not None:
        right_assems.append(reaction.leaving_assem_id)
    return f'{" + ".join(left_assems)} -> {" + ".join(right_assems)}'
