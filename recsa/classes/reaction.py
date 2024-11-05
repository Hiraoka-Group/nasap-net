from dataclasses import asdict, dataclass
from typing import ClassVar

from .assembly import Assembly


@dataclass
class IntraReaction:
    init_assem_id: str | int
    entering_assem_id: ClassVar[None] = None
    product_assem_id: str | int
    leaving_assem_id: str | int | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    metal_kind: str
    leaving_kind: str
    entering_kind: str
    duplicate_count: int

    def to_dict(self):
        d = asdict(self)
        d['entering_assem_id'] = self.entering_assem_id
        return d


@dataclass
class InterReaction:
    init_assem_id: str | int
    entering_assem_id: str | int
    product_assem_id: str | int
    leaving_assem_id: str | int | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    metal_kind: str
    leaving_kind: str
    entering_kind: str
    duplicate_count: int

    def to_dict(self):
        return asdict(self)


@dataclass
class IntraReactionEmbedded:
    init_assem: Assembly
    entering_assem: ClassVar[None] = None
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    metal_kind: str
    leaving_kind: str
    entering_kind: str
    duplicate_count: int


@dataclass
class InterReactionEmbedded:
    init_assem: Assembly
    entering_assem: Assembly
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    metal_kind: str
    leaving_kind: str
    entering_kind: str
    duplicate_count: int
