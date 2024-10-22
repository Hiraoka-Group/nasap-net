from collections.abc import Mapping

from recsa import (Assembly, ComponentStructure, InterReactionInit,
                   IntraReactionInit, MleKind, ReactionInit)
from recsa.algorithms.bindsite_equivalence import (AssemblyId, BindsiteToRoot,
                                                   ComponentKind,
                                                   RootToBindsites)
from recsa.algorithms.isomorphic_assembly_search import (
    IsomorphismFound, find_isomorphic_assembly)
from recsa.algorithms.mle_equivalence import MleToRoot, RootToMles
from recsa.algorithms.reverse_reaction_archives.inter import \
    get_reverse_inter_reaction
from recsa.algorithms.reverse_reaction_archives.intra import \
    get_reverse_intra_reaction
from recsa.algorithms.reverse_reaction_archives.rev_mle_kind import \
    get_rev_mle_kind

__all__ = ['get_reverse_reaction']


def get_reverse_reaction(
        reaction_init: ReactionInit, 
        product: Assembly, leaving: Assembly | None,
        id_to_assembly: Mapping[str, Assembly],
        hash_to_ids: Mapping[str, set[AssemblyId]],
        component_structures: Mapping[str, ComponentStructure],
        bindsite_to_root_maps: Mapping[
            tuple[AssemblyId, ComponentKind], BindsiteToRoot],
        root_to_bindsites_maps: Mapping[
            tuple[AssemblyId, ComponentKind], RootToBindsites],
        mle_to_root_maps: Mapping[tuple[AssemblyId, MleKind], MleToRoot],
        root_to_mle_maps: Mapping[tuple[AssemblyId, MleKind], RootToMles],
        ) -> ReactionInit | None:
    product_isom_result = find_isomorphic_assembly(
        product, id_to_assembly, hash_to_ids, component_structures)
    
    # Invalid reaction; the product is out of the assembly space
    if not product_isom_result.found:
        return None
    assert isinstance(product_isom_result, IsomorphismFound)

    rev_mle_kind = get_rev_mle_kind(reaction_init.mle_kind)

    # Case when the reverse reaction is intra-molecular
    if leaving is None:
        return get_reverse_intra_reaction(
            rev_mle_kind, reaction_init, product_isom_result,
            mle_to_root_maps, root_to_mle_maps)

    # Case when the reverse reaction is inter-molecular
    assert leaving is not None
    leaving_isom_result = find_isomorphic_assembly(
        leaving, id_to_assembly, hash_to_ids, component_structures)
    
    # Invalid reaction; the leaving assembly is out of the assembly space
    if not leaving_isom_result.found:
        return None
    assert isinstance(leaving_isom_result, IsomorphismFound)

    return get_reverse_inter_reaction(
        rev_mle_kind, reaction_init, 
        product_isom_result, leaving_isom_result,
        bindsite_to_root_maps, root_to_bindsites_maps,
        id_to_assembly
        )
