from typing import Mapping

from nasap_net import Assembly, Component
from reverse_reaction_pairing.core import Reaction, _A, _C


def _generate_reverse_reaction(
        reaction: Reaction,
        assemblies: Mapping[_A, Assembly],
        components: Mapping[_C, Component]
        ) -> Reaction:
    """Generate a reverse reaction from a given reaction."""
    raise NotImplementedError()
