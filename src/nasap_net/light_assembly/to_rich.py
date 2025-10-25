from collections.abc import Mapping
from typing import TypeVar

from nasap_net.models import Assembly, Component
from nasap_net.types import ID
from .models import LightAssembly

_T = TypeVar('_T', bound=ID)

def convert_light_assembly_to_rich_one(
        light_assembly: LightAssembly,
        components: Mapping[str, Component],
) -> Assembly:
    return Assembly(
        components={
            comp_id: components[comp_kind]
            for comp_id, comp_kind in light_assembly.components.items()
        },
        bonds=light_assembly.bonds,
        id_=light_assembly.id_or_none,
    )


def convert_light_assemblies_to_rich_ones(
        light_assemblies: Mapping[_T, LightAssembly],
        components: Mapping[str, Component],
) -> dict[ID, Assembly]:
    return {
        assembly_id: convert_light_assembly_to_rich_one(light_assembly, components)
        for assembly_id, light_assembly in light_assemblies.items()
    }
