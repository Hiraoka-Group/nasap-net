from dataclasses import dataclass

from nasap_net.models import Assembly, BindingSite
from nasap_net.types import ID


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

    @property
    def init_assem_id(self) -> ID:
        """Return the ID of the initial assembly.

        Errors if the ID is not set.
        """
        return self.init_assem.id_

    @property
    def entering_assem_id(self) -> ID | None:
        """Return the ID of the entering assembly, or None if there is none.

        Errors if the ID is not set.
        """
        if self.entering_assem is None:
            return None
        return self.entering_assem.id_

    @property
    def product_assem_id(self) -> ID:
        """Return the ID of the product assembly.

        Errors if the ID is not set.
        """
        return self.product_assem.id_

    @property
    def leaving_assem_id(self) -> ID | None:
        """Return the ID of the leaving assembly, or None if there is none.

        Errors if the ID is not set.
        """
        if self.leaving_assem is None:
            return None
        return self.leaving_assem.id_


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
