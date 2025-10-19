from collections.abc import Iterable, Mapping

import yaml

from nasap_net.light_assembly import LightAssembly
from nasap_net.models import Bond, Component
from nasap_net.types import ID


class AssemblyLightLoader(yaml.SafeLoader):
    component_context: Mapping[str, Component] = {}

    def ignore_aliases(self, data):
        return True


def _light_assembly_constructor(loader: yaml.Loader, node: yaml.Node) -> LightAssembly:
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


yaml.add_constructor('!LightAssembly', _light_assembly_constructor, Loader=AssemblyLightLoader)
