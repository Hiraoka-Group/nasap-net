from collections.abc import Mapping
from typing import TypeVar

from nasap_net import Component
from nasap_net.algorithms import are_equivalent_binding_site_lists
from nasap_net.reaction_pairing.core import Assembly
from ._models import _MLE

_A = TypeVar("_A", int, str)  # Assembly ID
_C = TypeVar('_C', int, str)  # Component ID


def _are_equivalent_mles(
        init_assembly: Assembly,
        entering_assembly: Assembly | None,
        binding_site_trio1: _MLE,
        binding_site_trio2: _MLE,
        components: Mapping[_C, Component]
        ) -> bool:
    """Check if two reactions of the same assemblies are equivalent."""
    # TODO: 事前条件を docstring に明示（例：Assembly ID の一致は確認済み）

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
        return True
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
