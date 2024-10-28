import pytest

from recsa import (Assembly, InterReaction, InterReactionEmbedded,
                   IntraReaction, IntraReactionEmbedded,
                   embed_assemblies_into_reaction)


def test_inter():
    REACTION = InterReaction(
        'MLX', 'L', 'ML2', 'X',
        'M1.a', 'X1.a', 'L1.a',
        'M', 'X', 'L', 2
    )

    ID_TO_ASSEMBLY = {
        'MLX': Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},
                        [('M1.a', 'L1.a'), ('M1.b', 'X1.a')]),
        'L': Assembly({'L1': 'L'}),
        'ML2': Assembly({'M1': 'M', 'L1': 'L', 'L2': 'L'},
                        [('M1.a', 'L1.a'), ('M1.b', 'L2.a')]),
        'X': Assembly({'X1': 'X'}),
    }
        
    embed_reaction = embed_assemblies_into_reaction(
        REACTION, ID_TO_ASSEMBLY)
    
    assert embed_reaction == InterReactionEmbedded(
        ID_TO_ASSEMBLY['MLX'], ID_TO_ASSEMBLY['L'],
        ID_TO_ASSEMBLY['ML2'], ID_TO_ASSEMBLY['X'],
        'M1.a', 'X1.a', 'L1.a',
        'M', 'X', 'L', 2
    )


def test_intra():
    REACTION = IntraReaction(
        'MLX', 'ML', 'X',
        'M1.a', 'X1.a', 'L1.b',
        'M', 'X', 'L', 1
    )

    ID_TO_ASSEMBLY = {
        'MLX': Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},
                        [('M1.a', 'L1.a'), ('M1.b', 'X1.a')]),
        'ML': Assembly({'M1': 'M', 'L1': 'L'},
                        [('M1.a', 'L1.a'), ('M1.b', 'L1.b')]),
        'X': Assembly({'X1': 'X'}),
    }
    
    embed_reaction = embed_assemblies_into_reaction(
        REACTION, ID_TO_ASSEMBLY)
    
    assert embed_reaction == IntraReactionEmbedded(
        ID_TO_ASSEMBLY['MLX'], ID_TO_ASSEMBLY['ML'], ID_TO_ASSEMBLY['X'],
        'M1.a', 'X1.a', 'L1.b',
        'M', 'X', 'L', 1
    )


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
