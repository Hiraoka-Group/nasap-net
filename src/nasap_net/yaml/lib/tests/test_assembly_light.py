import pytest

from nasap_net.light_assembly import LightAssembly
from nasap_net.models import Bond
from nasap_net.yaml.lib import dump_light_assemblies, \
    load_light_assemblies


@pytest.fixture
def MX2():
    return LightAssembly(
        id_='MX2',
        components={'X0': 'X', 'M0': 'M', 'X1': 'X'},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)])

@pytest.fixture
def dumped_MX2():
    return """!LightAssembly
components: {M0: M, X0: X, X1: X}
bonds:
- [M0, 0, X0, 0]
- [M0, 1, X1, 0]
id: MX2
"""


def test_dump(MX2, dumped_MX2):
    dumped = dump_light_assemblies(MX2)
    assert dumped == dumped_MX2


def test_load(MX2, dumped_MX2):
    loaded = load_light_assemblies(dumped_MX2)  # type: ignore
    assert loaded == MX2


def test_round_trip():
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

    dumped_assemblies = dump_light_assemblies(assemblies)
    loaded_assemblies = load_light_assemblies(dumped_assemblies)
    assert loaded_assemblies == assemblies
