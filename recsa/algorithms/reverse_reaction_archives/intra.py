from collections.abc import Mapping

from recsa import IntraReactionInit, MleKind, ReactionInit
from recsa.algorithms.isomorphic_assembly_search import IsomorphismFound
from recsa.algorithms.isomorphism_application_to_mle import \
    apply_isomorphism_to_mle
from recsa.algorithms.mle_equivalence import AssemblyId, MleToRoot, RootToMles

__all__ = ['get_reverse_intra_reaction']


def get_reverse_intra_reaction(
        rev_mle_kind: MleKind,
        reaction_init: ReactionInit,
        product_isom_result: IsomorphismFound,
        mle_to_root_maps: Mapping[tuple[AssemblyId, MleKind], MleToRoot],
        root_to_mle_maps: Mapping[tuple[AssemblyId, MleKind], RootToMles],
        ) -> IntraReactionInit:
    rev_init_assem_id = product_isom_result.isomer_id

    product_to_rev_init_isomorphism = product_isom_result.isomorphism
    product_mle_bindsites = reaction_init.mle_bindsite
    rev_mle_bindsites = apply_isomorphism_to_mle(
        product_mle_bindsites, product_to_rev_init_isomorphism)

    mle_bindsite_to_root = mle_to_root_maps[(rev_init_assem_id, rev_mle_kind)]

    rev_mle_root = mle_bindsite_to_root[rev_mle_bindsites]

    root_to_mle = root_to_mle_maps[(rev_init_assem_id, rev_mle_kind)]
    equiv_count = len(root_to_mle[rev_mle_root])

    return IntraReactionInit(
        mle_kind=rev_mle_kind,
        init_assembly_id=rev_init_assem_id,
        mle_bindsite=rev_mle_root,
        duplicate_count=equiv_count
        )
