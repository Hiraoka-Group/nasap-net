from nasap_net import (Assembly, InterReaction, InterReactionRich,
                       IntraReaction, IntraReactionRich, InterOrIntra)


def embed_assemblies_into_reaction(
        reaction: IntraReaction | InterReaction,
        id_to_assembly: dict[int, Assembly]
        ) -> IntraReactionRich | InterReactionRich:
    """Embed the assemblies into the reaction."""
    if reaction.inter_or_intra == InterOrIntra.INTRA:
        assert isinstance(reaction, IntraReaction)
        return IntraReactionRich.from_reaction(
            reaction, id_to_assembly)
    else:
        assert isinstance(reaction, InterReaction)
        return InterReactionRich.from_reaction(
            reaction, id_to_assembly)
