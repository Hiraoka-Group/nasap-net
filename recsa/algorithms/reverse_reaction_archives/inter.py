from collections.abc import Mapping

from recsa import (Assembly, InterReactionInit, MleBindsite, MleKind,
                   ReactionInit)
from recsa.algorithms.bindsite_equivalence import (AssemblyId, BindsiteToRoot,
                                                   ComponentKind,
                                                   RootToBindsites)
from recsa.algorithms.isomorphic_assembly_search import IsomorphismFound

__all__ = ['get_reverse_inter_reaction']


def get_reverse_inter_reaction(
        rev_mle_kind: MleKind,
        reaction_init: ReactionInit,
        product_isom_result: IsomorphismFound,
        leaving_isom_result: IsomorphismFound,
        bindsite_to_root_maps: Mapping[
            tuple[AssemblyId, ComponentKind], BindsiteToRoot],
        root_to_bindsite_maps: Mapping[
            tuple[AssemblyId, ComponentKind], RootToBindsites],
        id_to_assembly: Mapping[str, Assembly]
        ) -> InterReactionInit:
    rev_init_assem_id = product_isom_result.isomer_id
    rev_entering_assem_id = leaving_isom_result.isomer_id

    product_to_rev_init_isomorphism = product_isom_result.isomorphism

    init_metal_bindsite = reaction_init.mle_bindsite.metal
    init_leaving_bindsite = reaction_init.mle_bindsite.leaving
    init_entering_bindsite = reaction_init.mle_bindsite.entering
    if isinstance(reaction_init, InterReactionInit):
        init_metal_bindsite = f'init_{init_metal_bindsite}'
        init_leaving_bindsite = f'init_{init_leaving_bindsite}'
        init_entering_bindsite = f'entering_{init_entering_bindsite}'

    rev_metal_bindsite = product_to_rev_init_isomorphism[
        init_metal_bindsite]
    
    rev_init_metal_root_map = bindsite_to_root_maps[
        (rev_init_assem_id, rev_mle_kind.metal)]
    rev_metal_root = rev_init_metal_root_map[rev_metal_bindsite]

    rev_init = id_to_assembly[rev_init_assem_id]
    rev_leaving_root = rev_init.get_connected_bindsite(
        rev_metal_root)
    # NOTE: The leaving root should be the bindsite that is connected 
    # to the metal root in the reverse reaction.
    assert rev_leaving_root is not None

    leaving_to_rev_entering_isomorphism = leaving_isom_result.isomorphism
    rev_entering_bindsite = leaving_to_rev_entering_isomorphism[
        init_leaving_bindsite]

    rev_entering_root_map = bindsite_to_root_maps[
        (rev_entering_assem_id, rev_mle_kind.entering)]
    rev_entering_root = rev_entering_root_map[rev_entering_bindsite]

    rev_init_root_to_bindsites = root_to_bindsite_maps[
        (rev_init_assem_id, rev_mle_kind.metal)]
    rev_entering_root_to_bindsites = root_to_bindsite_maps[
        (rev_entering_assem_id, rev_mle_kind.entering)]
    equiv_metal_count = len(
        rev_init_root_to_bindsites[rev_metal_root])
    equiv_entering_count = len(
        rev_entering_root_to_bindsites[rev_entering_root])

    return InterReactionInit(
        mle_kind=rev_mle_kind,
        init_assembly_id=rev_init_assem_id,
        entering_assembly_id=rev_entering_assem_id,
        mle_bindsite=MleBindsite(
            metal=rev_metal_root,
            leaving=rev_leaving_root,
            entering=rev_entering_root
            ),
        duplicate_count=(equiv_metal_count * equiv_entering_count)
        )
