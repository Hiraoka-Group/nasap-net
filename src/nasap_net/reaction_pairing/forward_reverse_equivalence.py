from nasap_net.models import Reaction
from nasap_net.reaction_equivalence import reactions_equivalent

from .sample_rev_generation import generate_sample_rev_reaction


def is_forward_reverse_equivalent(reaction: Reaction) -> bool:
    """Check if the reaction is forward-reverse equivalent."""
    return reactions_equivalent(
        reaction,
        generate_sample_rev_reaction(reaction)
        )
