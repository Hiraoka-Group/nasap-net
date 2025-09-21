from abc import ABC, abstractmethod
from dataclasses import asdict, dataclass
from enum import Enum, auto
from typing import ClassVar, Literal


class InterOrIntra(Enum):
    INTER = auto()
    INTRA = auto()


class ReactionBase(ABC):
    @property
    @abstractmethod
    def inter_or_intra(self) -> InterOrIntra:
        """Whether the reaction is intra- or inter-molecular."""
        pass

    @property
    @abstractmethod
    def num_of_reactants(self) -> int:
        """Number of reactants in the reaction."""
        pass

    @property
    @abstractmethod
    def num_of_products(self) -> int:
        """Number of products in the reaction."""
        pass


@dataclass
class IntraReaction(ReactionBase):
    init_assem_id: int
    entering_assem_id: ClassVar[None] = None
    product_assem_id: int
    leaving_assem_id: int | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int

    @property
    def inter_or_intra(self) -> InterOrIntra:
        return InterOrIntra.INTRA

    def to_dict(self):
        d = asdict(self)
        d['entering_assem_id'] = self.entering_assem_id
        return d
    
    @property
    def num_of_reactants(self) -> Literal[1]:
        """Number of reactants in the reaction."""
        return 1
    
    @property
    def num_of_products(self) -> Literal[1, 2]:
        """Number of products in the reaction."""
        if self.leaving_assem_id is None:
            return 1
        return 2


@dataclass
class InterReaction:
    init_assem_id: int
    entering_assem_id: int
    product_assem_id: int
    leaving_assem_id: int | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int

    @property
    def inter_or_intra(self) -> InterOrIntra:
        return InterOrIntra.INTER

    def to_dict(self):
        return asdict(self)
    
    @property
    def num_of_reactants(self) -> Literal[2]:
        """Number of reactants in the reaction."""
        return 2
    
    @property
    def num_of_products(self) -> Literal[1, 2]:
        """Number of products in the reaction."""
        if self.leaving_assem_id is None:
            return 1
        return 2


