import yaml

from nasap_net.models import Assembly, AuxEdge, BindingSite, Bond, Component


class AssemblyDumper(yaml.SafeDumper): pass


def _assembly_representer(dumper: yaml.Dumper, data: Assembly) -> yaml.Node:
    mapping: dict = {
        'components': dict(sorted(data.components.items())),
        'bonds': sorted(data.bonds),
    }
    if data.id_or_none is not None:
        mapping['id'] = data.id
    return dumper.represent_mapping('!Assembly', mapping)

def _component_representer(
        dumper: yaml.Dumper, data: Component) -> yaml.Node:
    return dumper.represent_mapping('!Component', {
        'kind': data.kind,
        'binding_sites': sorted(str(s) for s in data.site_ids),
        'aux_edges': sorted(data.aux_edges) if data.aux_edges else [],
    })

def _binding_site_representer(dumper: yaml.Dumper, data: BindingSite) -> yaml.Node:
    return dumper.represent_mapping('!BindingSite', {
        'component_id': data.component_id,
        'site_id': data.site_id,
    })

def _aux_edge_representer(dumper: yaml.Dumper, data: AuxEdge) -> yaml.Node:
    site_id1, site_id2 = data.site_ids
    mapping = {
        'site_id1': site_id1,
        'site_id2': site_id2,
    }
    if data.kind is not None:
        mapping['kind'] = data.kind
    return dumper.represent_mapping('!AuxEdge', mapping)

def _bond_representer(dumper: yaml.Dumper, data: Bond) -> yaml.Node:
    site1, site2 = data.sites
    return dumper.represent_list([
        site1.component_id,
        site1.site_id,
        site2.component_id,
        site2.site_id,
    ])


yaml.add_representer(Assembly, _assembly_representer, Dumper=AssemblyDumper)
yaml.add_representer(Component, _component_representer, Dumper=AssemblyDumper)
yaml.add_representer(BindingSite, _binding_site_representer, Dumper=AssemblyDumper)
yaml.add_representer(AuxEdge, _aux_edge_representer, Dumper=AssemblyDumper)
yaml.add_representer(Bond, _bond_representer, Dumper=AssemblyDumper)
