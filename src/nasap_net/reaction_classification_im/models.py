from functools import cached_property
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

    def forms_ring(self) -> bool:
        """Whether this reaction forms any rings."""
        return self.forming_ring_size is not None

    def breaks_ring(self) -> bool:
        """Whether this reaction breaks any rings."""
        return self.breaking_ring_size is not None

    @cached_property
    def forming_ring_size(self) -> int | None:
        """The minimum size of rings formed in this reaction,
        or None if no rings are formed.
        """
        return get_min_forming_ring_size(self)

    @cached_property
    def breaking_ring_size(self) -> int | None:
        """The minimum size of rings broken in this reaction,
        or None if no rings are broken.
        """
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
