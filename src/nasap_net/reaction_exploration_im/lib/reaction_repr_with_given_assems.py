from typing import Iterable

from .isomorphic_assembly_search import \
    _AssemblyNotFoundError, find_isomorphic_assembly
from ..models import Reaction
from ...models import Assembly


class _ReactionOutOfScopeError(Exception):
    pass


def _represent_reaction_with_given_assemblies(
        reaction: Reaction,
        assemblies: Iterable[Assembly],
        ) -> Reaction:
    # Cond-1: The product assembly must exist in the provided assemblies.
    try:
        isom_product_assem = find_isomorphic_assembly(
            reaction.product_assem, assemblies)
    except _AssemblyNotFoundError as e:
        raise _ReactionOutOfScopeError("Product assembly not found") from e

    if reaction.leaving_assem is None:
        return Reaction(
            init_assem=reaction.init_assem,
            entering_assem=reaction.entering_assem,
            product_assem=isom_product_assem,
            leaving_assem=None,
            metal_bs=reaction.metal_bs,
            leaving_bs=reaction.leaving_bs,
            entering_bs=reaction.entering_bs,
            duplicate_count=reaction.duplicate_count
        )

    # Cond-2: The leaving assembly must exist in the provided assemblies.
    try:
        isom_leaving_assem = find_isomorphic_assembly(
            reaction.leaving_assem, assemblies)
    except _AssemblyNotFoundError as e:
        raise _ReactionOutOfScopeError("Leaving assembly not found") from e

    return Reaction(
        init_assem=reaction.init_assem,
        entering_assem=reaction.entering_assem,
        product_assem=isom_product_assem,
        leaving_assem=isom_leaving_assem,
        metal_bs=reaction.metal_bs,
        leaving_bs=reaction.leaving_bs,
        entering_bs=reaction.entering_bs,
        duplicate_count=reaction.duplicate_count
    )
