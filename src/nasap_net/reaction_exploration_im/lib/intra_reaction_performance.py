from nasap_net.reaction_exploration_im.models import Assembly, MLEWithDup
from .separation import \
    separate_if_possible


def perform_intra_reaction(
        assembly: Assembly,
        mle_with_dup: MLEWithDup
        ) -> tuple[Assembly, Assembly | None]:
    """Perform an intra-molecular reaction on the given assembly."""
    mle = mle_with_dup  # For brevity

    raw_product = (
        assembly
        .remove_bond(mle.metal, mle.leaving)
        .add_bond(mle.metal, mle.entering)
    )

    return separate_if_possible(raw_product, mle.metal.component_id)
