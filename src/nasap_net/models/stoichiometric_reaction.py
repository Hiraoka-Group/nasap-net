from dataclasses import dataclass
from typing import Self

from nasap_net.types import ID
from .reaction import Reaction


@dataclass(frozen=True)
class StoichiometricReaction:
    """A stoichiometric representation of a reaction between assemblies."""
    reactant1: ID
    reactant2: ID | None
    product1: ID
    product2: ID | None
    duplicate_count: int
    id_: ID | None = None

    def __post_init__(self):
        if self.duplicate_count <= 0:
            raise ValueError("duplicate_count must be positive")
        if self.reactant1 is None:
            raise ValueError("reactant1 must not be None")
        if self.product1 is None:
            raise ValueError("product1 must not be None")

    def __str__(self):
        equation = self.equation_str
        dup = self.duplicate_count
        return f'{equation} (x{dup})'

    def __repr__(self):
        equation = self.equation_str
        if self.id_ is None:
            return f'<{self.__class__.__name__} ({equation})>'
        return f'<{self.__class__.__name__} ID={self.id_} ({equation})>'

    @property
    def equation_str(self) -> str:
        """Return a string representation of the reaction equation."""
        def side_to_str(a: ID, b: ID | None) -> str:
            if b is not None:
                return f'{a} + {b}'
            return f'{a}'
        left = side_to_str(self.reactant1, self.reactant2)
        right = side_to_str(self.product1, self.product2)
        return f'{left} -> {right}'

    @classmethod
    def from_reaction(cls, reaction: Reaction) -> Self:
        """Create a StoichiometricReaction from a Reaction instance."""
        return cls(
            reactant1=reaction.init_assem_id,
            reactant2=reaction.entering_assem_id,
            product1=reaction.product_assem_id,
            product2=reaction.leaving_assem_id,
            duplicate_count=reaction.duplicate_count,
            id_=reaction.id_or_none,
        )
