from typing import TypeAlias

import pytest

from recsa import (Assembly, Component, InterReaction, IntraReaction,
                   explore_reactions)
from recsa.algorithms import are_equivalent_reaction_sets

Reaction: TypeAlias = IntraReaction | InterReaction


@pytest.fixture
def component_structures():
    return {
        'L': Component(['a', 'b']),
        'M': Component(['a', 'b']),
        'X': Component(['a']),
    }


@pytest.fixture
def id_to_assembly():
    return {
        # MX2: X0(a)-(a)M0(b)-(a)X1
        0: Assembly(
            {'M0': 'M', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'X1.a')]
        ),
        1: Assembly({'L0': 'L'}),  # L: (a)L0(b)
        2: Assembly({'X0': 'X'}),  # X: (a)X0
        # MLX: (a)L0(b)-(a)M0(b)-(a)X0
        3: Assembly(
            {'M0': 'M', 'L0': 'L', 'X0': 'X'},
            [('L0.b', 'M0.a'), ('M0.b', 'X0.a')]
        ),
        # ML2: (a)L0(b)-(a)M0(b)-(a)L1(b)
        4: Assembly(
            {'M0': 'M', 'L0': 'L', 'L1': 'L'},
            [('L0.b', 'M0.a'), ('M0.b', 'L1.a')]
        ),
        # M2L2X: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)
        5: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L', 'X0': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'L1.a')]
        ),
        # M2LX2: X0(a)-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)X1
        6: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'X0': 'X', 'X1': 'X'},
            [('X0.a', 'M0.a'), ('M0.b', 'L0.a'), ('L0.b', 'M1.a'),
             ('M1.b', 'X1.a')]
        ),
        # M2L2-ring: //-(a)M0(b)-(a)L0(b)-(a)M1(b)-(a)L1(b)-//
        7: Assembly(
            {'M0': 'M', 'M1': 'M', 'L0': 'L', 'L1': 'L'},
            [('M0.b', 'L0.a'), ('L0.b', 'M1.a'), ('M1.b', 'L1.a'),
             ('L1.b', 'M0.a')]
        ),
    }


def test_comprehensive_reaction_sets(component_structures, id_to_assembly):
    result = explore_reactions(
        id_to_assembly,
        metal_kind='M', leaving_kind='X', entering_kind='L',
        component_structures=component_structures
    )

    # All "X to L" reactions among the assemblies in id_to_assembly
    # including intra- and inter-molecular reactions:
    expected: dict[str, Reaction] = {
        # Intra-molecular reactions
        'M2L2X -> M2L2-ring + X': IntraReaction(
            init_assem_id=5, 
            product_assem_id=7, leaving_assem_id=2, 
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L1.b',
            duplicate_count=1,
        ),
        # Inter-molecular reactions
        'MX2 + L -> MLX + X': InterReaction(
            init_assem_id=0, entering_assem_id=1,
            product_assem_id=3, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=4,
        ),
        'MX2 + MLX -> M2LX2 + X': InterReaction(
            init_assem_id=0, entering_assem_id=3,
            product_assem_id=6, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=2,
        ),
        'MX2 + ML2 -> M2L2X + X': InterReaction(
            init_assem_id=0, entering_assem_id=4,
            product_assem_id=5, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=4,
        ),
        'MLX + L -> ML2 + X': InterReaction(
            init_assem_id=3, entering_assem_id=1,
            product_assem_id=4, leaving_assem_id=2,
            metal_bs='M0.b', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=2,
        ),
        'MLX + MLX -> M2L2X + X': InterReaction(
            init_assem_id=3, entering_assem_id=3,
            product_assem_id=5, leaving_assem_id=2,
            metal_bs='M0.b', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=2,
        ),
        'M2LX2 + L -> M2L2X + X': InterReaction(
            init_assem_id=6, entering_assem_id=1,
            product_assem_id=5, leaving_assem_id=2,
            metal_bs='M0.a', leaving_bs='X0.a', entering_bs='L0.a',
            duplicate_count=4,
        ),
    }

    assert are_equivalent_reaction_sets(
        result, list(expected.values()),
        id_to_assembly=id_to_assembly,
        component_structures=component_structures
    ), "The reaction sets are not equivalent."


if __name__ == "__main__":
    pytest.main([__file__, '-v'])
