from dataclasses import asdict, dataclass
from typing import Generic, TypeVar

from nasap_net import StoichiometricReaction
from .const import Column

_T = TypeVar('_T', int, str)  # Assembly ID type
_R = TypeVar('_R', int, str)  # Reaction ID type

T = TypeVar('T', bound='StoichiometricReactionRow')


@dataclass(frozen=True)
class StoichiometricReactionRow(Generic[_T, _R]):
    reactant1: _T
    reactant2: _T | None
    product1: _T
    product2: _T | None
    duplicate_count: int
    id_: _R | None

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_stoichiometric_reaction(
            cls: type[T],
            reaction: StoichiometricReaction,
    ) -> T:
        return cls(
            reactant1=reaction.reactant1,
            reactant2=reaction.reactant2,
            product1=reaction.product1,
            product2=reaction.product2,
            duplicate_count=reaction.duplicate_count,
            id_=reaction.id_or_none,
        )

    @classmethod
    def from_dict(
            cls: type[T],
            data: dict,
            *,
            assembly_id_type: type[_T],
            reaction_id_type: type[_R],
    ) -> T:
        return cls(
            reactant1=assembly_id_type(data[Column.REACTANT1.value]),
            reactant2=(
                assembly_id_type(data[Column.REACTANT2.value])
                if data[Column.REACTANT2.value] is not None else None
            ),
            product1=assembly_id_type(
                data[Column.PRODUCT1.value]
            ),
            product2=(
                assembly_id_type(data[Column.PRODUCT2.value])
                if data[Column.PRODUCT2.value] is not None else None
            ),
            duplicate_count=int(data[Column.DUPLICATE_COUNT.value]),
            id_=(
                reaction_id_type(data[Column.ID_.value])
                if data.get(Column.ID_.value) is not None else None
            ),
        )
