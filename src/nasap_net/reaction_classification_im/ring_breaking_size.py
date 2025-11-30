from nasap_net.models import Reaction
from nasap_net.reaction_pairing_im.sample_rev_generation import \
    generate_sample_rev_reaction
from .ring_formation_size import get_min_forming_ring_size


def get_min_breaking_ring_size(reaction: Reaction) -> int | None:
    """Determine the minimum ring size broken by a reaction.

    The "ring size" is defined as half the number of components involved
    in the ring.

    Examples:
     - M4L4 ring = size of 4
     - M3L3 ring = size of 3

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
