from collections.abc import Iterable, Iterator

from recsa import Assembly, Component

from .loading import CapParams
from .multi_bindsites import cap_bindsites


def cap_bindsites_for_multi_assemblies(
        assemblies: Iterable[Assembly],
        components: dict[str, Component],
        cap_params: CapParams
        ) -> Iterator[Assembly]:
    for assembly in assemblies:
        cap_bindsites(
            assembly, components, 
            cap_params.component_kind_to_be_capped,
            cap_params.cap_component_kind, cap_params.cap_bindsite,
            copy=False)
        yield assembly
