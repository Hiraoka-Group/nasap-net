from nasap_net.models import Reaction
from nasap_net.reaction_pairing_im.sample_rev_generation import \
    generate_sample_rev_reaction
from .ring_formation_size import get_min_forming_ring_size


def get_min_breaking_ring_size(reaction: Reaction) -> int | None:
    """Determine the minimum ring size broken by a reaction.

    Returns None if the reaction does not break a ring.

    Parameters
    ----------
    reaction : Reaction
        The reaction to analyze.

    Returns
    -------
    int | None
        The minimum ring size broken, or None if no ring is broken.
    """
    # TODO: Optimize this; currently we generate the full reverse reaction,
    #   which might be inefficient.
    rev = generate_sample_rev_reaction(reaction)
    return get_min_forming_ring_size(rev)
