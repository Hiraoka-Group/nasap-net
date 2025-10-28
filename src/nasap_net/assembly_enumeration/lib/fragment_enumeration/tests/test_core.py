import pytest

from nasap_net.assembly_enumeration.lib.fragment_enumeration import \
    enumerate_fragments
from nasap_net.assembly_enumeration.lib.symmetry_operation import \
    SymmetricOperations
from nasap_net.models import Assembly, AuxEdge, Bond, Component


@pytest.fixture
def M() -> Component:
    return Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])

@pytest.fixture
def L() -> Component:
    return Component(kind='L', sites=[0, 1])

@pytest.fixture
def X() -> Component:
    return Component(kind='X', sites=[0])

@pytest.fixture
def MX2(M, X) -> Assembly:
    return Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)])


def test(MX2, M, X):
    frags = enumerate_fragments(MX2)
    assert frags == {
        Assembly(
            {'M0': M, 'X0': X, 'X1': X},
            [Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
        ),
        Assembly({'M0': M, 'X0': X}, [Bond('M0', 0, 'X0', 0)]),
        Assembly({'M0': M, 'X1': X}, [Bond('M0', 1, 'X1', 0)]),
        Assembly({'M0': M}, []),
        Assembly({'X0': X}, []),
        Assembly({'X1': X}, []),
    }


def test_symmetry_operations(MX2, M, X):
    symmetry_operations = [
        {
            'M0': 'M0',
            'X0': 'X1',
            'X1': 'X0',
        }
    ]
    frags = enumerate_fragments(MX2, symmetry_operations)
    assert frags == {
        Assembly(
            {'M0': M, 'X0': X, 'X1': X},
            [Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)]
        ),
        Assembly({'M0': M, 'X0': X}, [Bond('M0', 0, 'X0', 0)]),
        Assembly({'M0': M}, []),
        Assembly({'X0': X}, []),
    }


def test_M4L4():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    M4L4 = Assembly(
        components={
            'M0': M, 'M1': M, 'M2': M, 'M3': M,
            'L0': L, 'L1': L, 'L2': L, 'L3': L,
        },
        bonds=[
            Bond('M0', 1, 'L0', 0), Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0), Bond('L1', 1, 'M2', 0),
            Bond('M2', 1, 'L2', 0), Bond('L2', 1, 'M3', 0),
            Bond('M3', 1, 'L3', 0), Bond('L3', 1, 'M0', 0),
        ]
    )
    #  M3---L2---M2
    #  |         |
    #  L3        L1
    #  |         |
    #  M0---L0---M1
    sym_ops = SymmetricOperations()
    sym_ops.add_cyclic_permutation(
        'C_4',[['M0', 'M1', 'M2', 'M3'], ['L0', 'L1', 'L2', 'L3']]
    )
    sym_ops.add_product('C_2', ['C_4', 'C_4'])
    sym_ops.add_product('C_4^3', ['C_4', 'C_4', 'C_4'])
    sym_ops.add_cyclic_permutation(
        'C_2x',[['M0', 'M1'], ['M2', 'M3'], ['L0'], ['L1', 'L3'], ['L2']]
    )
    sym_ops.add_product('C_2y', ['C_2x', 'C_2'])
    sym_ops.add_product('C_2(1)', ['C_2x', 'C_4'])
    sym_ops.add_product('C_2(2)', ['C_2x', 'C_4^3'])
    frags = enumerate_fragments(M4L4, list(sym_ops.resolved.values()))
    assert len(frags) == 13


def test_M2L4():
    #                 |                                     |
    #                (1)                                   (0)
    #                 L2                                    L2
    #                (0)                                   (1)
    #                 |                                     |
    #                (2)                                   (2)
    # --(1)L3(0)---(3)M0(1)---(0)L1(1)--    --(0)L3(1)---(3)M1(1)---(1)L1(0)--
    #                (0)                                   (0)
    #                 |                                     |
    #                (0)                                   (1)
    #                 L0                                    L0
    #                (1)                                   (0)
    #                 |                                     |
    M = Component(
        kind='M', sites=[0, 1, 2, 3],
        aux_edges=[AuxEdge(0, 1), AuxEdge(1, 2), AuxEdge(2, 3), AuxEdge(3, 0)])
    L = Component(kind='L', sites=[0, 1])
    M2L4 = Assembly(
        components={
            'M0': M, 'M1': M,
            'L0': L, 'L1': L, 'L2': L, 'L3': L,
        },
        bonds=[
            Bond('M0', 0, 'L0', 0), Bond('M0', 1, 'L1', 0),
            Bond('M0', 2, 'L2', 0), Bond('M0', 3, 'L3', 0),
            Bond('M1', 0, 'L0', 1), Bond('M1', 1, 'L1', 1),
            Bond('M1', 2, 'L2', 1), Bond('M1', 3, 'L3', 1),
        ]
    )

    sym_ops = SymmetricOperations()
    sym_ops.add_cyclic_permutation(
        'C_4',[['M0'], ['M1'], ['L0', 'L1', 'L2', 'L3']]
    )
    sym_ops.add_product('C_2', ['C_4', 'C_4'])
    sym_ops.add_product('C_4^3', ['C_4', 'C_4', 'C_4'])
    sym_ops.add_cyclic_permutation(
        'C_2x',[['M0', 'M1'], ['L0', 'L2'], ['L1'], ['L3']]
    )
    sym_ops.add_product('C_2y', ['C_2x', 'C_2'])
    sym_ops.add_product('C_2(1)', ['C_2x', 'C_4'])
    sym_ops.add_product('C_2(2)', ['C_2x', 'C_4^3'])
    sym_ops.add_cyclic_permutation(
        'i', [['M0', 'M1'], ['L0', 'L2'], ['L1', 'L3']]
    )
    sym_ops.add_product('S_4', ['i', 'C_4'])
    sym_ops.add_product('sigma', ['i', 'C_2'])
    sym_ops.add_product('S_4^3', ['i', 'C_4^3'])
    sym_ops.add_product('sigma_x', ['i', 'C_2x'])
    sym_ops.add_product('sigma_y', ['i', 'C_2y'])
    sym_ops.add_product('sigma_1', ['i', 'C_2(1)'])
    sym_ops.add_product('sigma_2', ['i', 'C_2(2)'])
    frags = enumerate_fragments(M2L4, list(sym_ops.resolved.values()))
    assert len(frags) == 28
