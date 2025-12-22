from collections import defaultdict
from dataclasses import dataclass
from typing import Self

from nasap_net.exceptions import IDNotSetError
from nasap_net.types import ID
from .reaction import Reaction


@dataclass(frozen=True, init=False)
class StoichiometricReaction:
    """A stoichiometric representation of a reaction between assemblies."""
    reactant1: ID
    reactant2: ID | None
    product1: ID
    product2: ID | None
    duplicate_count: int
    _id: ID | None

    def __init__(
        self,
        reactant1: ID,
        reactant2: ID | None,
        product1: ID,
        product2: ID | None,
        duplicate_count: int,
        id_: ID | None = None,
    ):
        if duplicate_count <= 0:
            raise ValueError("duplicate_count must be positive")
        if reactant1 is None:
            raise ValueError("reactant1 must not be None")
        if product1 is None:
            raise ValueError("product1 must not be None")
        object.__setattr__(self, 'reactant1', reactant1)
        object.__setattr__(self, 'reactant2', reactant2)
        object.__setattr__(self, 'product1', product1)
        object.__setattr__(self, 'product2', product2)
        object.__setattr__(self, 'duplicate_count', duplicate_count)
        object.__setattr__(self, '_id', id_)

    def __str__(self):
        equation = self.equation_str
        dup = self.duplicate_count
        return f'{equation} (x{dup})'

    def __repr__(self):
        equation = self.equation_str
        if self._id is None:
            return f'<{self.__class__.__name__} ({equation})>'
        return f'<{self.__class__.__name__} ID={self._id} ({equation})>'

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

    @property
    def id_(self) -> ID:
        """Return the ID. Raise IDNotSetError if not set."""
        if self._id is None:
            raise IDNotSetError("StoichiometricReaction ID is not set.")
        return self._id

    @property
    def id_or_none(self) -> ID | None:
        """Return the ID of the reaction, or None if not set."""
        return self._id

    @property
    def reactants(self) -> dict[ID, int]:
        """
        Return a dictionary of reactant IDs and their counts.
        For example, for A + B -> C, returns {A: 1, B: 1}.
        """
        counts: defaultdict[ID, int] = defaultdict(int)
        counts[self.reactant1] += 1
        if self.reactant2 is not None:
            counts[self.reactant2] += 1
        return dict(counts)

    @property
    def products(self) -> dict[ID, int]:
        """
        Return a dictionary of product IDs and their counts.
        For example, for A + B -> C, returns {C: 1}.
        """
        counts: defaultdict[ID, int] = defaultdict(int)
        counts[self.product1] += 1
        if self.product2 is not None:
            counts[self.product2] += 1
        return dict(counts)

    @property
    def changes(self) -> dict[ID, int]:
        """
        Return a dictionary of ID to net change (products - reactants).
        Reactants are negative, products are positive.
        For example, for A + B -> C, returns {A: -1, B: -1, C: 1}.
        """
        changes: defaultdict[ID, int] = defaultdict(int)
        for k, v in self.reactants.items():
            changes[k] -= v
        for k, v in self.products.items():
            changes[k] += v
        return dict(changes)

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
