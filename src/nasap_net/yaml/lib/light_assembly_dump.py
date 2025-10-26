from typing import Any

import yaml

from nasap_net.models import Bond, LightAssembly


def dump_light_assemblies(assemblies: Any) -> str:
    """Dump light assemblies to a YAML string."""
    return yaml.dump(
        assemblies,
        Dumper=_LightAssemblyDumper,
        sort_keys=False,
        default_flow_style=None,
    )


class _LightAssemblyDumper(yaml.SafeDumper):
    def ignore_aliases(self, _):
        return True


def _light_assembly_representer(
        dumper: _LightAssemblyDumper, data: LightAssembly
) -> yaml.MappingNode:
    mapping: dict = {
        'components': dict(sorted(data.components.items())),
        'bonds': sorted(data.bonds),
    }
    if data.id_or_none is not None:
        mapping['id'] = data.id
    return dumper.represent_mapping('!LightAssembly', mapping)


def _bond_representer(
        dumper: _LightAssemblyDumper, data: Bond
) -> yaml.SequenceNode:
    site1, site2 = sorted(data.sites)
    return dumper.represent_list([
        site1.component_id,
        site1.site_id,
        site2.component_id,
        site2.site_id,
    ])


yaml.add_representer(
    LightAssembly, _light_assembly_representer, Dumper=_LightAssemblyDumper
)
yaml.add_representer(Bond, _bond_representer, Dumper=_LightAssemblyDumper)
