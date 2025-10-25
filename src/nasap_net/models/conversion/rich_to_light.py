from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from typing import TypeVar

from nasap_net.types import ID
from ..assembly import Assembly
from ..component import Component
from ..light_assembly import LightAssembly


@dataclass(frozen=True)
class ConversionResult:
    light_assemblies: Mapping[ID, LightAssembly]
    components: Mapping[str, Component]


class InconsistentComponentKindError(Exception):
    """Raised when there are inconsistent definitions for a component kind,
    i.e., the same kind name corresponds to different component structures.
    """
    def __init__(
            self,
            component_kind: str,
            message: str = 'Inconsistent definitions for component kind.'
    ) -> None:
        self.component_kind = component_kind
        super().__init__(f'{message}: Kind: "{component_kind}".')


_T = TypeVar('_T', bound=ID)

def convert_assemblies_to_light_ones(
        assemblies: Mapping[_T, Assembly],
) -> ConversionResult:
    light_assemblies = _assemblies_to_light_assemblies(assemblies)

    try:
        components = _extract_components(assemblies.values())
    except InconsistentComponentKindError as e:
        raise InconsistentComponentKindError(e.component_kind) from None

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
                if comp != components[comp.kind]:
                    raise InconsistentComponentKindError(comp.kind)
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
