from collections.abc import Iterable
from dataclasses import dataclass
from functools import total_ordering
from typing import Self

from nasap_net.models import Assembly, Bond
from nasap_net.types import ID


@total_ordering
@dataclass(frozen=True, init=False)
class LightBond:
    component_ids: frozenset[ID]

    def __init__(self, comp_id1: ID, comp_id2: ID) -> None:
        object.__setattr__(
            self, 'component_ids', frozenset({comp_id1, comp_id2})
        )

    def __lt__(self, other):
        if not isinstance(other, LightBond):
            return NotImplemented
        return sorted(self.component_ids) < sorted(other.component_ids)

    @classmethod
    def from_bond(cls, bond: Bond) -> Self:
        site1, site2 = bond.sites
        return cls(site1.component_id, site2.component_id)


@total_ordering
@dataclass(frozen=True, init=False)
class Fragment:
    components: frozenset[ID]
    bonds: frozenset[LightBond]

    def __init__(
            self,
            components: Iterable[ID],
            bonds: Iterable[LightBond],
    ) -> None:
        object.__setattr__(self, 'components', frozenset(components))
        object.__setattr__(self, 'bonds', frozenset(bonds))
        self._validate()

    def __lt__(self, other):
        if not isinstance(other, Fragment):
            return NotImplemented
        if self.components != other.components:
            return sorted(self.components) < sorted(other.components)
        return sorted(self.bonds) < sorted(other.bonds)

    def _validate(self):
        for bond in self.bonds:
            for comp_id in bond.component_ids:
                if comp_id not in self.components:
                    raise ValueError(
                        f"Bond references non-existent component ID: {comp_id}"
                    )

    def copy_with(
            self,
            components: Iterable[ID] | None = None,
            bonds: Iterable[LightBond] | None = None,
    ) -> Self:
        return self.__class__(
            components=(
                components if components is not None else self.components
            ),
            bonds=bonds if bonds is not None else self.bonds,
        )

    @classmethod
    def from_assembly(cls, assembly: Assembly) -> Self:
        components = assembly.components.keys()
        bonds = [LightBond.from_bond(bond) for bond in assembly.bonds]
        return cls(components=components, bonds=bonds)
