from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import Self

from nasap_net.exceptions import IDNotSetError
from nasap_net.types import ID
from .assembly import Assembly
from .bond import Bond


@dataclass(frozen=True, init=False)
class LightAssembly:
    components: dict[ID, str]
    bonds: frozenset[Bond]
    _id: ID | None

    def __init__(
            self,
            components: Mapping[ID, str],
            bonds: Iterable[Bond],
            id_: ID | None = None,
            ):
        object.__setattr__(self, 'components', components)
        object.__setattr__(self, 'bonds', frozenset(bonds))
        object.__setattr__(self, '_id', id_)

    @property
    def id(self) -> ID:
        if self._id is None:
            raise IDNotSetError('LightAssembly ID is not set.')
        return self._id

    @property
    def id_or_none(self) -> ID | None:
        return self._id

    @classmethod
    def from_assembly(cls, assembly: Assembly) -> Self:
        components = {
            comp_id: comp.kind
            for comp_id, comp in assembly.components.items()
        }
        return cls(
            components=components,
            bonds=assembly.bonds,
            id_=assembly.id_or_none,
        )
