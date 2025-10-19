from dataclasses import dataclass
from typing import Iterable, Mapping

from nasap_net.models import Assembly, Component
from nasap_net.types import ID
from .models import LightAssembly


@dataclass(frozen=True)
class ConversionResult:
    light_assemblies: Mapping[ID, LightAssembly]
    components: Mapping[str, Component]


class InconsistentComponentKindError(Exception):
    """Raised when there are inconsistent definitions for a component kind,
    i.e., the same kind name corresponds to different component structures.
    """
    pass


def convert_assemblies_to_light_ones(
        assemblies: Mapping[ID, Assembly]) -> ConversionResult:
    light_assemblies = _assemblies_to_light_assemblies(assemblies)

    try:
        components = _extract_components(assemblies.values())
    except InconsistentComponentKindError:
        raise InconsistentComponentKindError(
            "Failed to convert assemblies to light assemblies due to "
            "inconsistent component kind definitions."
        ) from None

    return ConversionResult(
        light_assemblies=light_assemblies,
        components=components,
    )


def _extract_components(assemblies: Iterable[Assembly]) -> dict[str, Component]:
    components = {}
    for assembly in assemblies:
        for comp in assembly.components.values():
            if comp.kind in components:
                if comp != components[comp.kind]:
                    raise InconsistentComponentKindError(
                        f"Inconsistent definitions for component kind '{comp.kind}'.")
            else:
                components[comp.kind] = comp
    return components


def _assemblies_to_light_assemblies(
        assemblies: Mapping[ID, Assembly],
        ) -> Mapping[ID, LightAssembly]:
    return {
        assembly_id: LightAssembly.from_assembly(assembly)
        for assembly_id, assembly in assemblies.items()
    }
