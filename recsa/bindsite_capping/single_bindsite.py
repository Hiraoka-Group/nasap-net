from typing import Literal, overload

from recsa import Assembly, BindsiteIdConverter

__all__ = ['cap_single_bindsite']


def cap_single_bindsite(
        assembly: Assembly, target_bindsite: str,
        cap_id: str, cap_component_kind: str, cap_bindsite: str
        ) -> Assembly | None:
    """Add a leaving ligand (cap) to the assembly."""
    id_converter = BindsiteIdConverter()
    assembly = assembly.deepcopy()

    assembly = assembly.with_added_component(cap_id, cap_component_kind)
    assembly = assembly.with_added_bond(
        id_converter.local_to_global(cap_id, cap_bindsite), target_bindsite)

    return assembly
