from typing import Mapping

from nasap_net import Assembly, Component
from reverse_reaction_pairing.core import Reaction, _A, _C
from reverse_reaction_pairing.lib.mle import _MLE


def _determine_right_hand_side_mle(
        reaction: Reaction[_A],
        assemblies: Mapping[_A, Assembly],
        components: Mapping[_C, Component]
        ) -> _MLE:
    """Determine the binding site trio on the right-hand side of a reaction."""
    raise NotImplementedError()
