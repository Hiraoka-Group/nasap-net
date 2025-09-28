import pytest

from nasap_net import Assembly, Component
from nasap_net.reaction_pairing import Reaction, pair_reverse_reactions


@pytest.fixture
def components():
    return {
        'L': Component(['a', 'b']),
        'M': Component(['a', 'b']),
        'X': Component(['a']),
    }


@pytest.fixture
def assemblies():
    return {
        # MX2: X0(a)-(a)M0(b)-(a)X1
        'MX2': Assembly(
            {'M0': 'M', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'X1.a')]
        ),
        'L': Assembly({'L0': 'L'}),  # L: (a)L0(b)
        'X': Assembly({'X0': 'X'}),  # X: (a)X0
        # MLX: (a)L0(b)-(a)M0(b)-(a)X0
        'MLX': Assembly(
            {'M0': 'M', 'L0': 'L', 'X0': 'X'},
            [('L0.b', 'M0.a'), ('M0.b', 'X0.a')]
        ),
        # ML2: (a)L0(b)-(a)M0(b)-(a)L1(b)
        'ML2': Assembly(
            {'M0': 'M', 'L0': 'L', 'L1': 'L'},
            [('L0.b', 'M0.a'), ('M0.b', 'L1.a')]
        ),
        # M2L2X: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)
        'M2L2X': Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 'X0': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'L1.a')]
        ),
        # M2LX2: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)X1
        'M2LX2': Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'X1.a')]
        ),
        # M2L2-ring: //-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)-//
        'M2L2-ring': Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L'},
            [('M0.b', 'L0.a'), ('L0.b', 'M1.a'), ('M1.b', 'L1.a'),
             ('L1.b', 'M0.a')]
        ),
    }


def test_basic(components, assemblies):
    reactions = {
        '1f': Reaction(
            'MX2', 'L', 'MLX', 'X',
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a'),
        '1b': Reaction(
            'MLX', 'X', 'MX2', 'L',
            metal_bs='M0.a', leaving_bs='L0.b', entering_bs='X0.a'),
        '2f': Reaction(
            'MLX', 'L', 'ML2', 'X',
            metal_bs='M0.b', leaving_bs='X0.a', entering_bs='L0.a'),
        '2b': Reaction(
            'ML2', 'X', 'MLX', 'L',
            metal_bs='M0.a', leaving_bs='L0.b', entering_bs='X0.a'),
        }
    result = pair_reverse_reactions(reactions, assemblies, components)
    expected = {
        '1f': '1b',
        '1b': '1f',
        '2f': '2b',
        '2b': '2f',
        }
    assert result == expected
