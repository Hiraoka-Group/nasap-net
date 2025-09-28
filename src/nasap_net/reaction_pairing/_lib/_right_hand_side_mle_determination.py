from typing import Mapping

from nasap_net import Assembly, Component
from nasap_net.reaction_pairing import Reaction
from nasap_net.reaction_pairing._lib._models import _MLE
from nasap_net.types import A, C


def _determine_right_hand_side_mle(
        reaction: Reaction[A],
        assemblies: Mapping[A, Assembly],
        components: Mapping[C, Component]
        ) -> _MLE:
    """Determine the binding site trio on the right-hand side of a reaction."""
    raise NotImplementedError()
