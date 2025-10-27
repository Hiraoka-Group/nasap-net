from collections.abc import Mapping
from dataclasses import dataclass
from typing import TypeVar

from nasap_net.models import Assembly
from nasap_net.types import ID
from nasap_net.yaml.lib import dump_components, dump_semi_light_assemblies
from nasap_net.yaml.semi_light_assembly import \
    convert_assemblies_to_semi_light_ones

_T = TypeVar('_T', bound=ID)

def dump(assemblies: Mapping[_T, Assembly]) -> str:
    """Dump assemblies and components into a YAML string."""
    dumped = _dump_separately(assemblies)
    return '---\n'.join([dumped.components, dumped.assemblies])


@dataclass(frozen=True)
class _Dumped:
    assemblies: str
    components: str


def _dump_separately(
        assemblies: Mapping[_T, Assembly],
        ) -> _Dumped:
    res = convert_assemblies_to_semi_light_ones(assemblies)

    return _Dumped(
        assemblies=dump_semi_light_assemblies(
            dict(sorted(res.semi_light_assemblies.items()))
        ),
        components=dump_components(
            dict(sorted(res.components.items())),
        ),
    )
