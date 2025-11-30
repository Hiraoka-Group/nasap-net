from typing import Self

from nasap_net.models import Reaction
from .ring_breaking_size import get_min_breaking_ring_size
from .ring_formation_size import get_min_forming_ring_size


class ReactionToClassify(Reaction):
    """Dataclass representing a reaction to classify."""
    pass

    @property
    def metal_kind(self) -> str:
        """Return the kind of the metal binding site."""
        return self.init_assem.get_component_kind_of_site(self.metal_bs)

    @property
    def leaving_kind(self) -> str:
        """Return the kind of the leaving binding site."""
        return self.init_assem.get_component_kind_of_site(self.leaving_bs)

    @property
    def entering_kind(self) -> str:
        """Return the kind of the entering binding site."""
        assem = self.init_assem if self.is_intra() else self.entering_assem_strict
        return assem.get_component_kind_of_site(self.entering_bs)

    @property
    def forming_ring_size(self) -> int | None:
        """The size of the ring being formed, if applicable."""
        return get_min_forming_ring_size(self)

    @property
    def breaking_ring_size(self) -> int | None:
        """The size of the ring being broken, if applicable."""
        return get_min_breaking_ring_size(self)

    @classmethod
    def from_reaction(cls, reaction: Reaction) -> Self:
        """Create a ReactionToClassify from a Reaction."""
        return cls(
            init_assem=reaction.init_assem,
            entering_assem=reaction.entering_assem,
            product_assem=reaction.product_assem,
            leaving_assem=reaction.leaving_assem,
            metal_bs=reaction.metal_bs,
            leaving_bs=reaction.leaving_bs,
            entering_bs=reaction.entering_bs,
        )
