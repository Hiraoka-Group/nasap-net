import yaml

from nasap_net.models import Assembly, AuxEdge, Bond, Component
from nasap_net.yaml import AssemblyDumper


def test_assembly_dump_and_load():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    M_square = Component(
        kind='M(sq)', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])

    assemblies = {
        # MX2: X0(0)-(0)M0(1)-(0)X1
        'MX2': Assembly(
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]),
        'free_X': Assembly(components={'X0': X}, bonds=[]),
        # MLX: (0)L0(1)-(0)M0(1)-(0)X0
        'MLX': Assembly(
            components={'L0': L, 'M0': M, 'X0': X},
            bonds=[Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'X0', 0)]),
        'M(sq)X4': Assembly(
            components={'M0': M_square, 'X0': X, 'X1': X, 'X2': X, 'X3': X},
            bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0),
                   Bond('M0', 2, 'X2', 0), Bond('M0', 3, 'X3', 0)]),
        'M(sq)L2X2': Assembly(
            components={'M0': M_square, 'L0': L, 'L1': L, 'X0': X, 'X1': X},
            bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'L0', 0),
                   Bond('M0', 2, 'X1', 0), Bond('M0', 3, 'L1', 0)]),
    }
    dumped_assemblies = yaml.dump(
        assemblies, Dumper=AssemblyDumper, sort_keys=False,
        default_flow_style=None)
    print()
    print(dumped_assemblies)
    # TODO: implement loading test
