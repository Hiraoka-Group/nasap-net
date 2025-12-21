from collections.abc import Mapping
from dataclasses import dataclass, field

from frozendict import frozendict

from nasap_net.types import ID


@dataclass(frozen=True)
class StoichiometricReaction:
    """A stoichiometric representation of a reaction between assemblies."""
    reactants: frozendict[ID, int] = field(init=False)
    products: frozendict[ID, int] = field(init=False)
    duplicate_count: int
    id_: ID | None = None

    def __init__(
        self,
        reactants: Mapping[ID, int],
        products: Mapping[ID, int],
        duplicate_count: int,
        id_: ID | None = None,
    ):
        object.__setattr__(self, 'reactants', frozendict(reactants))
        object.__setattr__(self, 'products', frozendict(products))
        object.__setattr__(self, 'duplicate_count', duplicate_count)
        object.__setattr__(self, 'id_', id_)
        if duplicate_count <= 0:
            raise ValueError("duplicate_count must be positive")

    def __str__(self):
        equation = self.equation_str
        dup = self.duplicate_count
        return f'{equation} (x{dup})'

    def __repr__(self):
        equation = self.equation_str
        if self.id_ is None:
            return f'<{self.__class__.__name__} {equation}>'
        return f'<{self.__class__.__name__} ID={self.id_}: {equation}>'

    @property
    def equation_str(self) -> str:
        """Return a string representation of the reaction equation."""
        def side_to_str(side: Mapping[ID, int]) -> str:
            return ' + '.join(
                f'{v if v != 1 else ""}{k}' if v != 1 else f'{k}'
                for k, v in sorted(side.items())
            )
        left = side_to_str(self.reactants)
        right = side_to_str(self.products)
        return f'{left} -> {right}'
