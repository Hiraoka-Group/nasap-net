from collections.abc import Mapping

from nasap_net import Assembly
from nasap_net.classes.reaction import R_co, SupportsRichReaction


def embed_assemblies_into_reaction(
        reaction: SupportsRichReaction[R_co],
        id_to_assembly: Mapping[int, Assembly],
) -> R_co:
    """Embed the assemblies into the reaction."""
    return reaction.to_rich_reaction(id_to_assembly)


if __name__ == "__main__":
    from nasap_net import (InterReaction, IntraReaction, InterReactionRich,
                           IntraReactionRich)
    r_inter = InterReaction(
        0, 1, 2, 3,
        'M1.a', 'X1.a', 'L1.a', 2)
    r_intra = IntraReaction(
        0, 1, 2,
        'M1.a', 'X1.a', 'L1.b', 1)
    id_to_assem = {
        0: Assembly(),
        1: Assembly(),
        2: Assembly(),
        3: Assembly(),
    }
    r_inter_embedded = embed_assemblies_into_reaction(r_intra, id_to_assem)
    r_intra_embedded = embed_assemblies_into_reaction(r_intra, id_to_assem)
    assert isinstance(r_inter_embedded, InterReactionRich)
    assert isinstance(r_intra_embedded, IntraReactionRich)
    print("All tests passed.")
