from typing import Mapping

from nasap_net import Assembly, Component
from nasap_net.types import A, C
from ..models import Reaction, _MLE


def _determine_right_hand_side_mle(
        reaction: Reaction[A],
        assemblies: Mapping[A, Assembly],
        components: Mapping[C, Component]
        ) -> _MLE:
    """Determine the binding site trio on the right-hand side of a reaction."""
    raise NotImplementedError()
