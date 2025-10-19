import yaml

from nasap_net.light_assembly import LightAssembly
from nasap_net.models import Bond


class LightAssemblyDumper(yaml.SafeDumper):
    def ignore_aliases(self, data):
        return True


def _light_assembly_representer(
        dumper: yaml.Dumper, data: LightAssembly) -> yaml.Node:
    mapping: dict = {
        'components': dict(sorted(data.components.items())),
        'bonds': sorted(data.bonds),
    }
    if data.id_or_none is not None:
        mapping['id'] = data.id
    return dumper.represent_mapping('!LightAssembly', mapping)

def _bond_representer(dumper: yaml.Dumper, data: Bond) -> yaml.Node:
    site1, site2 = data.sites
    return dumper.represent_list([
        site1.component_id,
        site1.site_id,
        site2.component_id,
        site2.site_id,
    ])


yaml.add_representer(LightAssembly, _light_assembly_representer, Dumper=LightAssemblyDumper)
yaml.add_representer(Bond, _bond_representer, Dumper=LightAssemblyDumper)
