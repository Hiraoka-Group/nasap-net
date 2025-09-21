from dataclasses import dataclass
from functools import cached_property
from typing import ClassVar

from .assembly import Assembly


@dataclass(frozen=True)
class IntraReactionRich:
    init_assem: Assembly
    entering_assem: ClassVar[None] = None
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int

    @cached_property
    def metal_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.metal_bs)

    @cached_property
    def leaving_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.leaving_bs)

    @cached_property
    def entering_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.entering_bs)


@dataclass(frozen=True)
class InterReactionRich:
    init_assem: Assembly
    entering_assem: Assembly
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    duplicate_count: int

    @cached_property
    def metal_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.metal_bs)

    @cached_property
    def leaving_kind(self) -> str:
        return self.init_assem.get_component_kind_of_bindsite(
            self.leaving_bs)

    @cached_property
    def entering_kind(self) -> str:
        return self.entering_assem.get_component_kind_of_bindsite(
            self.entering_bs)
