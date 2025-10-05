from typing import TypeVar

from nasap_net.reaction_exploration_im.models import Assembly, MLEWithDup
from .separation import \
    separate_if_possible

_T = TypeVar('_T', bound=Assembly)


def perform_intra_reaction(
        assembly: _T,
        mle_with_dup: MLEWithDup
        ) -> tuple[_T, _T | None]:
    """Perform an intra-molecular reaction on the given assembly."""
    mle = mle_with_dup  # For brevity

    raw_product = (
        assembly
        .add_bond(mle.metal, mle.entering)
        .remove_bond(mle.metal, mle.leaving)
    )

    return separate_if_possible(raw_product, mle.metal)
