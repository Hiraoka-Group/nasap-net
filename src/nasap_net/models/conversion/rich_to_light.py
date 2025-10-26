from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import TypeVar

from nasap_net.types import ID
from ..assembly import Assembly
from ..component import Component
from ..component_consistency_check import check_component_consistency
from ..light_assembly import LightAssembly


@dataclass(frozen=True)
class ConversionResult:
    light_assemblies: Mapping[ID, LightAssembly]
    components: Mapping[str, Component]


_T = TypeVar('_T', bound=ID)

def convert_assemblies_to_light_ones(
        assemblies: Mapping[_T, Assembly],
) -> ConversionResult:
    light_assemblies = _assemblies_to_light_assemblies(assemblies)

    check_component_consistency(assemblies.values())
    components = _extract_components(assemblies.values())

    return ConversionResult(
        light_assemblies=light_assemblies,
        components=components,
    )


def _extract_components(
        assemblies: Iterable[Assembly],
) -> dict[str, Component]:
    components: dict[str, Component] = {}
    for assembly in assemblies:
        for comp in assembly.components.values():
            if comp.kind in components:
                assert comp == components[comp.kind]
            else:
                components[comp.kind] = comp
    return components


def _assemblies_to_light_assemblies(
        assemblies: Mapping[_T, Assembly],
        ) -> Mapping[ID, LightAssembly]:
    return {
        assembly_id: LightAssembly.from_assembly(assembly)
        for assembly_id, assembly in assemblies.items()
    }
