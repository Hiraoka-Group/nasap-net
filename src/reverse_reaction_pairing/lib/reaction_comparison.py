from collections.abc import Mapping
from dataclasses import dataclass
from typing import TypeVar

from nasap_net import Component
from nasap_net.algorithms import are_equivalent_binding_site_lists
from reverse_reaction_pairing.core import Assembly

_A = TypeVar("_A", int, str)  # Assembly ID
_C = TypeVar('_C', int, str)  # Component ID


@dataclass(frozen=True)
class BindingSiteTrio:
    metal: str
    leaving: str
    entering: str


def _are_equivalent_reactions(
        init_assembly: Assembly,
        entering_assembly: Assembly | None,
        binding_site_trio1: BindingSiteTrio,
        binding_site_trio2: BindingSiteTrio,
        components: Mapping[_C, Component]
        ) -> bool:
    """Check if two reactions of the same assemblies are equivalent."""
    # TODO: 事前条件を docstring に明示（例：Assembly ID の一致は確認済み）

    # Condition 3: Equivalent pair/trio of binding sites
    if entering_assembly is None:  # intra
        if not are_equivalent_binding_site_lists(
                init_assembly,
                (
                        binding_site_trio1.metal,
                        binding_site_trio1.leaving,
                        binding_site_trio1.entering),
                (
                        binding_site_trio2.metal,
                        binding_site_trio2.leaving,
                        binding_site_trio2.entering),
                components
                ):
            return False
    else:  # inter
        # Check for initial assembly
        if not are_equivalent_binding_site_lists(
                init_assembly,
                (binding_site_trio1.metal, binding_site_trio1.leaving),
                (binding_site_trio2.metal, binding_site_trio2.leaving),
                components
                ):
            return False
        # Check for entering assembly
        if not are_equivalent_binding_site_lists(
                entering_assembly,
                (binding_site_trio1.entering,),
                (binding_site_trio2.entering,),
                components
                ):
            return False

    return True
