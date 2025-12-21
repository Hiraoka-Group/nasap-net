from dataclasses import dataclass
from typing import TypeVar

from nasap_net import StoichiometricReaction
from nasap_net.types import ID

T = TypeVar('T', bound='StoichiometricReactionRow')


@dataclass(frozen=True)
class StoichiometricReactionRow:
    reactant1: ID
    reactant2: ID | None
    product1: ID
    product2: ID | None
    duplicate_count: int
    id_: ID | None = None

    @classmethod
    def from_stoichiometric_reaction(cls: type[T], r: StoichiometricReaction) -> T:
        return cls(
            reactant1=r.reactant1,
            reactant2=r.reactant2,
            product1=r.product1,
            product2=r.product2,
            duplicate_count=r.duplicate_count,
            id_=r.id_,
        )

    def to_dict(self) -> dict:
        d = {
            'reactant1': self.reactant1,
            'reactant2': self.reactant2,
            'product1': self.product1,
            'product2': self.product2,
            'duplicate_count': self.duplicate_count,
            'id': self.id_,
        }
        return d

    @classmethod
    def from_dict(cls: type[T], d: dict) -> T:
        return cls(
            reactant1=d['reactant1'],
            reactant2=d.get('reactant2'),
            product1=d['product1'],
            product2=d.get('product2'),
            duplicate_count=int(d['duplicate_count']),
            id_=d.get('id'),
        )

    def to_stoichiometric_reaction(self) -> StoichiometricReaction:
        return StoichiometricReaction(
            reactant1=self.reactant1,
            reactant2=self.reactant2,
            product1=self.product1,
            product2=self.product2,
            duplicate_count=self.duplicate_count,
            id_=self.id_,
        )
