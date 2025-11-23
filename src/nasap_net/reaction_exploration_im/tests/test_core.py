from nasap_net.models import Assembly, Bond, Component, MLEKind
from nasap_net.reaction_exploration_im import explore_reactions


def test():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    assemblies = [
        # MX2: X0(0)-(0)M0(1)-(0)X1
        Assembly(
            id_='MX2',
            components={'X0': X, 'M0': M, 'X1': X},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]),
        Assembly(id_='free_L', components={'L0': L}, bonds=[]),
        Assembly(id_='free_X', components={'X0': X}, bonds=[]),
        # MLX: (0)L0(1)-(0)M0(1)-(0)X0
        Assembly(
            id_='MLX',
            components={'L0': L, 'M0': M, 'X0': X},
            bonds=[Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'X0', 0)]),
        # ML2: (0)L0(1)-(0)M0(1)-(0)L1(1)
        Assembly(
            id_='ML2',
            components={'L0': L, 'M0': M, 'L1': L},
            bonds=[Bond('L0', 1, 'M0', 0), Bond('M0', 1, 'L1', 0)]),
        # M2L2X: X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
        Assembly(
            id_='M2L2X',
            components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0),
                   Bond('L0', 1, 'M1', 0), Bond('M1', 1, 'L1', 0)]),
        # M2LX2: X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)X1
        Assembly(
            id_='M2LX2',
            components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'X1': X},
            bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'L0', 0),
                   Bond('L0', 1, 'M1', 0), Bond('M1', 1, 'X1', 0)]),
        # M2L2-ring: //-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)-//
        Assembly(
            id_='M2L2-ring',
            components={'M0': M, 'L0': L, 'M1': M, 'L1': L},
            bonds=[Bond('M0', 1, 'L0', 0), Bond('L0', 1, 'M1', 0),
                   Bond('M1', 1, 'L1', 0), Bond('L1', 1, 'M0', 0)]),
    ]
    result = set(explore_reactions(assemblies, [MLEKind('M', 'X', 'L')]))
    # TODO: add more detailed checks
    assert len(result) == 7
