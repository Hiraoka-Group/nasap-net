from dataclasses import dataclass
from typing import ClassVar


@dataclass
class IntraReaction:
    init_assem_id: str
    entering_assem_id: ClassVar[None] = None
    product_assem_id: str
    leaving_assem_id: str | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    metal_kind: str
    leaving_kind: str
    entering_kind: str
    duplicate_count: int


@dataclass
class InterReaction:
    init_assem_id: str
    entering_assem_id: str
    product_assem_id: str
    leaving_assem_id: str | None
    metal_bs: str
    leaving_bs: str
    entering_bs: str
    metal_kind: str
    leaving_kind: str
    entering_kind: str
    duplicate_count: int