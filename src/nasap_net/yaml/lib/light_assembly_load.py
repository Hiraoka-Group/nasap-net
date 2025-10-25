from collections.abc import Iterable, Mapping

import yaml

from nasap_net.light_assembly import LightAssembly
from nasap_net.models import Bond, Component
from nasap_net.types import ID


def load_light_assemblies(yaml_str: str) -> dict[ID, LightAssembly]:
    """Load light assemblies from a YAML string."""
    return yaml.load(yaml_str, Loader=_LightAssemblyLoader)  # type: ignore


class _LightAssemblyLoader(yaml.SafeLoader):
    component_context: Mapping[str, Component] = {}

    def ignore_aliases(self, _):
        return True


def _light_assembly_constructor(
        loader: _LightAssemblyLoader,
        node: yaml.Node,
) -> LightAssembly:
    assert isinstance(node, yaml.MappingNode)
    mapping = loader.construct_mapping(node, deep=True)
    components: dict[ID, str] = mapping['components']
    bonds: list[Bond] = [_construct_bond(b) for b in mapping['bonds']]
    assembly_id: str | None = mapping.get('id')
    return LightAssembly(
        components=components,
        bonds=bonds,
        id_=assembly_id,
    )


def _construct_bond(bonds: Iterable[ID]) -> Bond:
    comp_id1, site_id1, comp_id2, site_id2 = bonds
    return Bond(comp_id1, site_id1, comp_id2, site_id2)


yaml.add_constructor(
    '!LightAssembly', _light_assembly_constructor,
    Loader=_LightAssemblyLoader
)
