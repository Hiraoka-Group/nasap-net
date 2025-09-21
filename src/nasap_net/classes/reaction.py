from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum, auto
from typing import ClassVar, Literal, Mapping, Protocol, TypeVar

from .assembly import Assembly
from .rich_reaction import InterReactionRich, IntraReactionRich, \
    RichReactionBase


class InterOrIntra(Enum):
    INTER = auto()
    INTRA = auto()


R_co = TypeVar("R_co", bound=RichReactionBase, covariant=True)


class SupportsRichReaction(Protocol[R_co]):
    """Protocol for reactions that can be converted to a rich reaction."""
    def to_rich_reaction(
        self, id_to_assembly: Mapping[int, Assembly]
        ) -> R_co: ...


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

    @abstractmethod
    def to_rich_reaction(self, id_to_assembly: dict[int, Assembly]) -> RichReactionBase:
        """Convert to a rich reaction by embedding assemblies."""
        pass


@dataclass
class InterReaction(ReactionBase):
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

    def to_rich_reaction(
            self, id_to_assembly: Mapping[int, Assembly]
            ) -> InterReactionRich:
        return InterReactionRich.from_reaction(self, id_to_assembly)


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

    def to_rich_reaction(
            self, id_to_assembly: Mapping[int, Assembly]
            ) -> IntraReactionRich:
        return IntraReactionRich.from_reaction(self, id_to_assembly)
