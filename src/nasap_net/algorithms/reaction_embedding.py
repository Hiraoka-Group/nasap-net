from nasap_net import (Assembly, ReactionBase, RichReactionBase)


def embed_assemblies_into_reaction(
        reaction: ReactionBase,
        id_to_assembly: dict[int, Assembly]
        ) -> RichReactionBase:
    """Embed the assemblies into the reaction."""
    return reaction.to_rich_reaction(id_to_assembly)
