from nasap_net.models import Assembly, BindingSite, Bond, Component, Reaction
from nasap_net.reaction_classification_im import ReactionToClassify


def test_basic():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])

    MX2 = Assembly(
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_L = Assembly(components={'L0': L}, bonds=[])
    MLX = Assembly(
        components={'L0': L, 'M0': M, 'X1': X},
        bonds=[Bond('L0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_X = Assembly(components={'X0': X}, bonds=[])

    reaction = Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L0', 0),
    )

    reaction_to_classify_1 = ReactionToClassify.from_reaction(reaction)
    assert isinstance(reaction_to_classify_1, ReactionToClassify)

    reaction_to_classify_2 = reaction.as_reaction_to_classify()
    assert isinstance(reaction_to_classify_2, ReactionToClassify)

    assert reaction_to_classify_1 == reaction_to_classify_2

    assert reaction_to_classify_1.metal_kind == 'M'
    assert reaction_to_classify_1.leaving_kind == 'X'
    assert reaction_to_classify_1.entering_kind == 'L'

    assert reaction_to_classify_1.forming_ring_size is None
    assert reaction_to_classify_1.breaking_ring_size is None


def test_forming_ring_size():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])

    # X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
    M2L2X = Assembly(
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0),
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
        ],
    )
    # //-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)-//
    M2L2_ring = Assembly(
        components={'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
            Bond('L1', 1, 'M0', 0),
        ],
    )
    free_X = Assembly(components={'X0': X}, bonds=[])

    reaction = Reaction(
        init_assem=M2L2X,
        entering_assem=None,
        product_assem=M2L2_ring,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('X0', 0),
        entering_bs=BindingSite('L1', 1),
    )

    reaction_to_classify = ReactionToClassify.from_reaction(reaction)

    assert reaction_to_classify.forming_ring_size == 2
    assert reaction_to_classify.breaking_ring_size is None


def test_breaking_ring_size():
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])

    # //-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)-//
    M2L2_ring = Assembly(
        components={'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
            Bond('L1', 1, 'M0', 0),
        ],
    )
    free_X = Assembly(components={'X0': X}, bonds=[])
    # X0(0)-(0)M0(1)-(0)L0(1)-(0)M1(1)-(0)L1(1)
    M2L2X = Assembly(
        components={'X0': X, 'M0': M, 'L0': L, 'M1': M, 'L1': L},
        bonds=[
            Bond('X0', 0, 'M0', 0),
            Bond('M0', 1, 'L0', 0),
            Bond('L0', 1, 'M1', 0),
            Bond('M1', 1, 'L1', 0),
        ],
    )

    reaction = Reaction(
        init_assem=M2L2_ring,
        entering_assem=free_X,
        product_assem=M2L2X,
        leaving_assem=None,
        metal_bs=BindingSite('M0', 0),
        leaving_bs=BindingSite('L1', 1),
        entering_bs=BindingSite('X0', 0),
    )

    reaction_to_classify = ReactionToClassify.from_reaction(reaction)

    assert reaction_to_classify.forming_ring_size is None
    assert reaction_to_classify.breaking_ring_size == 2
