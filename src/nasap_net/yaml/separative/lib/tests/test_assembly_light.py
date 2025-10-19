import yaml

from nasap_net.light_assembly import LightAssembly
from nasap_net.models import Bond
from nasap_net.yaml.separative.lib import AssemblyLightLoader, \
    LightAssemblyDumper


def test_assembly_light_dump_and_load():
    assemblies = {
        # MX2: X0(0)-(0)M0(1)-(0)X1
        'MX2': LightAssembly(
            id_='MX2',
            components={'X0': 'X', 'M0': 'M', 'X1': 'X'},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]),
        'free_X': LightAssembly(components={'X0': 'X'}, bonds=[]),
        # MLX: (0)L0(1)-(0)M0(1)-(0)X0
        'MLX': LightAssembly(
            components={'L0': 'L', 'M0': 'M', 'X0': 'X'},
            bonds=[Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'X0', 0)]),
        'M(sq)X4': LightAssembly(
            components={'M0': 'M_square', 'X0': 'X', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
            bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0),
                   Bond('M0', 2, 'X2', 0), Bond('M0', 3, 'X3', 0)]),
        'M(sq)L2X2': LightAssembly(
            components={'M0': 'M_square', 'L0': 'L', 'L1': 'L', 'X0': 'X', 'X1': 'X'},
            bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'L0', 0),
                   Bond('M0', 2, 'X1', 0), Bond('M0', 3, 'L1', 0)]),
    }

    dumped_assemblies = yaml.dump(
        assemblies, Dumper=LightAssemblyDumper, sort_keys=False,
        default_flow_style=None)
    loaded_assemblies = yaml.load(
        dumped_assemblies, Loader=AssemblyLightLoader)
    assert loaded_assemblies == assemblies
