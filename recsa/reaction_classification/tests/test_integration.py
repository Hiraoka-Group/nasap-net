"""Integration tests for reaction classification.

Each test utilizes the functions from recsa.reaction_classification.utils 
to construct a rule for reaction classification. The rule is then used to 
create a ReactionClassifier object, which is used to classify reactions.
"""

import pytest

from recsa import (Assembly, Component, InterReactionEmbedded,
                   IntraReactionEmbedded, ReactionClassifier)
from recsa.reaction_classification.utils import (calc_nth_site_on_metal,
                                                 inter_or_intra)

ReactionEmbedded = IntraReactionEmbedded | InterReactionEmbedded


def test_classification_by_inter_or_intra():
    def rule(reaction: ReactionEmbedded):
        if inter_or_intra(reaction) == "intra":
            return "intra"
        return "inter"
    
    classifier = ReactionClassifier(rule)

    intra = IntraReactionEmbedded(
        init_assem=Assembly(), product_assem=Assembly(),
        leaving_assem=Assembly(), 
        metal_bs='', leaving_bs='', entering_bs='',
        metal_kind='', leaving_kind='', entering_kind='',
        duplicate_count=0
        )
    result = classifier.classify(intra)
    assert result == "intra"

    inter = InterReactionEmbedded(
        init_assem=Assembly(), entering_assem=Assembly(),
        product_assem=Assembly(), leaving_assem=Assembly(),
        metal_bs='', leaving_bs='', entering_bs='',
        metal_kind='', leaving_kind='', entering_kind='',
        duplicate_count=0
        )
    result = classifier.classify(inter)
    assert result == "inter"


@pytest.fixture
def MLX():
    return Assembly({'M1': 'M', 'L1': 'L', 'X1': 'X'},
                    [('M1.a', 'L1.a'), ('M1.b', 'X1.a')])

@pytest.fixture
def L():
    return Assembly({'L1': 'L'})

@pytest.fixture
def ML2():
    return Assembly({'M1': 'M', 'L1': 'L', 'L2': 'L'},
                    [('M1.a', 'L1.a'), ('M1.b', 'L2.a')])

@pytest.fixture
def X():
    return Assembly({'X1': 'X'})

@pytest.fixture
def X_to_L(MLX, L, ML2, X):
    """MLX + L -> ML2 + X (L-X exchange)"""
    return InterReactionEmbedded(
        init_assem=MLX, entering_assem=L,
        product_assem=ML2, leaving_assem=X,
        metal_bs='M1.a', leaving_bs='X1.a', entering_bs='L1.a',
        metal_kind='M', leaving_kind='X', entering_kind='L',
        duplicate_count=2  # 1 (dup. on MLX) * 2 (dup. on L)
    )

@pytest.fixture
def L_to_L(MLX, L):
    """MLX + L -> MLX + L (L-L exchange)"""
    return InterReactionEmbedded(
        init_assem=MLX, entering_assem=L,
        product_assem=MLX, leaving_assem=L,
        metal_bs='M1.a', leaving_bs='L1.a', entering_bs='L1.a',
        metal_kind='M', leaving_kind='L', entering_kind='L',
        duplicate_count=2  # 1 (dup. on MLX) * 2 (dup. on L)
    )

@pytest.fixture
def comp_kind_to_obj():
    return {
        'M': Component(['a', 'b']),
        'L': Component(['a', 'b']),
        'X': Component(['a']),
    }


def test_classification_by_comp_kinds(X_to_L, L_to_L):
    def rule(reaction: ReactionEmbedded):
        entering = reaction.entering_kind
        leaving = reaction.leaving_kind
        return f'{leaving}_to_{entering}'
    
    classifier = ReactionClassifier(rule)

    result = classifier.classify(X_to_L)
    assert result == "X_to_L"

    result = classifier.classify(L_to_L)
    assert result == "L_to_L"


def test_by_nth_site_on_metal_with_entering_first(
        X_to_L, L_to_L, comp_kind_to_obj):
    def rule(reaction: ReactionEmbedded):
        source_comp = Component(['a', 'b'])
        nth_site_on_metal = calc_nth_site_on_metal(
            reaction, comp_kind_to_obj, 'entering_first')  # entering_first
        return f'{nth_site_on_metal}'
    
    classifier = ReactionClassifier(rule)

    # MLX + L -> ML2X (transition state) -> ML2 + X
    # L enters the 2nd site on M of ML
    assert classifier.classify(X_to_L) == '2'

    # MLX + L -> ML2X (transition state) -> MLX + L
    # L enters the 2nd site on M of ML
    assert classifier.classify(L_to_L) == '2'


def test_by_nth_site_on_metal_with_leaving_first(
        X_to_L, L_to_L, comp_kind_to_obj):
    def rule(reaction: ReactionEmbedded):
        source_comp = Component(['a', 'b'])
        nth_site_on_metal = calc_nth_site_on_metal(
            reaction, comp_kind_to_obj, 'leaving_first')  # leaving_first
        return f'{nth_site_on_metal}'
    
    classifier = ReactionClassifier(rule)

    # MLX + L -> ML + X + L (transition state) -> ML2 + X
    # L enters the 2nd site on M of ML
    assert classifier.classify(X_to_L) == '2'

    # MLX + L -> MX + L + L (transition state) -> MLX + L
    # L enters the 1st site on M of ML
    assert classifier.classify(L_to_L) == '1'


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
