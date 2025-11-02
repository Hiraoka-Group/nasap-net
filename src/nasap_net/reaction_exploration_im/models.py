from dataclasses import dataclass

from nasap_net.exceptions import NasapNetError
from nasap_net.models import Assembly, BindingSite
from nasap_net.types import ID


@dataclass(frozen=True)
class MLEKind:
    metal: str
    leaving: str
    entering: str


class DuplicationNotSetError(NasapNetError):
    pass


@dataclass(frozen=True, init=False)
class MLE:
    metal: BindingSite
    leaving: BindingSite
    entering: BindingSite
    _duplication: int | None = None

    def __init__(
            self,
            metal: BindingSite,
            leaving: BindingSite,
            entering: BindingSite,
            *,
            duplication: int | None = None
    ) -> None:
        object.__setattr__(self, 'metal', metal)
        object.__setattr__(self, 'leaving', leaving)
        object.__setattr__(self, 'entering', entering)
        object.__setattr__(self, '_duplication', duplication)

    @property
    def duplication(self) -> int:
        if self._duplication is None:
            raise DuplicationNotSetError("Duplication count is not set.")
        return self._duplication


@dataclass(frozen=True)
class Reaction:
    init_assem: Assembly
    entering_assem: Assembly | None
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: BindingSite
    leaving_bs: BindingSite
    entering_bs: BindingSite
    duplicate_count: int

    def __str__(self):
        equation = self.equation
        dup = self.duplicate_count
        return f'{equation} (x{dup})'

    def __repr__(self):
        equation = self.equation
        return f'<{self.__class__.__name__} {equation}>'

    @property
    def equation(self) -> str:
        """Return a string representation of the reaction equation.

        If an assembly ID is not set, '??' is used in its place.
        """
        init = _assembly_to_id(self.init_assem)
        entering = _assembly_to_id(self.entering_assem)
        product = _assembly_to_id(self.product_assem)
        leaving = _assembly_to_id(self.leaving_assem)

        left = f'{init}' if entering is None else f'{init} + {entering}'
        right = f'{product}' if leaving is None else f'{product} + {leaving}'

        return f'{left} -> {right}'


def _assembly_to_id(assembly: Assembly | None) -> ID | None:
    """Return the ID of the assembly, or '??' if not set, or None if assembly
    is None.
    """
    if assembly is None:
        return None
    if assembly.id_or_none is None:
        # ID not set
        return '??'
    return assembly.id_or_none
