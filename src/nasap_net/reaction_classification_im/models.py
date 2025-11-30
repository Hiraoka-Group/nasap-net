from functools import cached_property
from typing import Self

from nasap_net.models import Assembly, Reaction
from . import get_connection_count_of_kind
from .ring_breaking_size import get_min_breaking_ring_size
from .ring_formation_size import get_min_forming_ring_size
from ..reaction_pairing_im.sample_rev_generation import \
    generate_sample_rev_reaction


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
        return self.assem_with_entering_bs.get_component_kind_of_site(self.entering_bs)

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

    @cached_property
    def init_ligand_count_on_metal(self) -> int:
        """Return the number of ligands bound to the metal before reaction."""
        return get_connection_count_of_kind(
            assembly=self.init_assem,
            source_component_id=self.metal_bs.component_id,
            target_kind=self.entering_kind,
        )

    @cached_property
    def init_metal_count_on_ligand(self) -> int:
        """Return the number of metals bound to the entering ligand before reaction."""
        return get_connection_count_of_kind(
            assembly=self.assem_with_entering_bs,
            source_component_id=self.entering_bs.component_id,
            target_kind=self.metal_kind,
        )

    @cached_property
    def rev(self) -> 'ReactionToClassify':
        """Return the reverse reaction."""
        return generate_sample_rev_reaction(self).as_reaction_to_classify()

    @property
    def assem_with_entering_bs(self) -> Assembly:
        """Return the assembly that contains the entering binding site."""
        if self.is_inter():
            return self.entering_assem_strict
        return self.init_assem

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
