from typing import TypeAlias

import pytest

from recsa import (Assembly, Component, InterReactionEmbedded,
                   IntraReactionEmbedded)
from recsa.reaction_classification.utils import calc_nth_site_on_metal

ReactionEmbedded: TypeAlias = (
    IntraReactionEmbedded | InterReactionEmbedded)


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
    """MLX + L -> ML2 + X (X-L exchange)"""
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


def test_X_to_L_leaving_first(X_to_L, comp_kind_to_obj):
    # leaving_first: X leaves from MX2 before L enters (like SN1 reaction)
    # MLX + L -> ML + X + L (transition state) -> ML2 + X
    result = calc_nth_site_on_metal(
        X_to_L, comp_kind_to_obj, 'leaving_first')

    # L enters the 2nd site on M of ML
    assert result == 2


def test_X_to_L_entering_first(X_to_L, comp_kind_to_obj):
    # entering_first: L enters to MLX before X leaves (like SN2 reaction)
    # MLX + L -> ML2X (transition state) -> ML2 + X
    result = calc_nth_site_on_metal(
        X_to_L, comp_kind_to_obj, 'entering_first')

    # L enters the 2nd site on M of MLX
    assert result == 2


def test_L_to_L_leaving_first(L_to_L, comp_kind_to_obj):
    # leaving_first: X leaves from MX2 before L enters (like SN1 reaction)
    # MLX + L -> MX + L + L (transition state) -> MLX + L
    result = calc_nth_site_on_metal(
        L_to_L, comp_kind_to_obj, 'leaving_first')

    # L enters the 1st site on M of ML
    assert result == 1


def test_L_to_L_entering_first(L_to_L, comp_kind_to_obj):
    # entering_first: L enters to MLX before X leaves (like SN2 reaction)
    # MLX + L -> ML2X (transition state) -> MLX + L
    result = calc_nth_site_on_metal(
        L_to_L, comp_kind_to_obj, 'entering_first')

    # L enters the 2nd site on M of MLX
    assert result == 2


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
