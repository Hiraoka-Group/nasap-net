from typing import Mapping

from nasap_net import Assembly, Component
from nasap_net.algorithms import perform_inter_exchange, perform_intra_exchange
from nasap_net.types import A, C
from ..models import Reaction, _MLE


def _generate_sample_rev_mle(
        reaction: Reaction[A],
        assemblies: Mapping[A, Assembly],
        components: Mapping[C, Component]
        ) -> _MLE:
    """Determine the binding site trio on the right-hand side of a reaction."""
    if reaction.entering_assem_id is None:  # intra
        product, leaving = perform_intra_exchange(
            assemblies[reaction.init_assem_id],
            reaction.metal_bs, reaction.leaving_bs, reaction.entering_bs
            )
        rhs_metal_bs = reaction.metal_bs
        rhs_leaving_bs = reaction.leaving_bs
        rhs_entering_bs = reaction.entering_bs
    else:
        product, leaving = perform_inter_exchange(
            assemblies[reaction.init_assem_id],
            assemblies[reaction.entering_assem_id],
            reaction.metal_bs, reaction.leaving_bs, reaction.entering_bs
            )
        rhs_metal_bs = f'init_{reaction.metal_bs}'
        rhs_leaving_bs = f'init_{reaction.leaving_bs}'
        rhs_entering_bs = f'init_{reaction.entering_bs}'


    raise NotImplementedError()
