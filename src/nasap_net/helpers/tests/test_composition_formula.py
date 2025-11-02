from nasap_net.helpers import assign_default_assembly_ids, \
    generate_composition_formula
from nasap_net.models import Assembly, Component


def test_assign_default_assembly_ids():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])

    MX2 = Assembly(
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[],
    )
    MX2_2 = Assembly(
        components={'X0_2': X, 'M0_2': M, 'X1_2': X},
        bonds=[],
    )

    assert assign_default_assembly_ids([MX2, MX2_2]) == [
        Assembly(
            id_='MX2',
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[],
        ),
        Assembly(
            id_='MX2_2',
            components={'X0_2': X, 'M0_2': M, 'X1_2': X},
            bonds=[],
        ),
    ]


def test_composition_formula():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])

    MX2 = Assembly(
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[],
    )

    assert generate_composition_formula(MX2) == 'MX2'


def test_order():
    M = Component(kind='M', sites=[0, 1])
    X = Component(kind='X', sites=[0])

    MX2 = Assembly(
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[],
    )

    assert generate_composition_formula(MX2) == 'MX2'
    assert generate_composition_formula(MX2, order=['X', 'M']) == 'X2M'


def test_unspecified_components_are_sorted_alphabetically():
    A = Component(kind='A', sites=[0])
    B = Component(kind='B', sites=[0])
    C = Component(kind='C', sites=[0])
    D = Component(kind='D', sites=[0])

    ABCD = Assembly({'A0': A, 'B0': B, 'C0': C, 'D0': D}, bonds=[])

    assert generate_composition_formula(ABCD, order=['C', 'A']) == 'CA' + 'BD'
