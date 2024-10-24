import pytest

from recsa import Assembly, Component, LocalAuxEdge, MleBindsite, MleKind
from recsa.algorithms.mle_equivalence import compute_mle_equivalence_as_uf
from recsa.algorithms.mle_equivalence.as_uf import _update_mle_equivalence


def test__update_mle_equivalence():
    pass


def test_for_specific_assembly() -> None:
    MLX = Assembly(
        {'M1': 'M', 'L1': 'L', 'X1': 'X'},
        {('M1.a', 'L1.a'), ('M1.b', 'X1.a')}
    )
    MLE_KINDS = [
        MleKind(metal='M', entering='L', leaving='X'),
    ]
    COMPONENT_STRUCTURES = {
        'M': Component('M', {'a', 'b'}),
        'L': Component('L', {'a', 'b'}),
        'X': Component('X', {'a'})
    }
    mle_kind_to_uf = compute_mle_equivalence_as_uf(
        MLX, MLE_KINDS, COMPONENT_STRUCTURES)

    assert mle_kind_to_uf.keys() == {MleKind(metal='M', entering='L', leaving='X')}
    
    uf = mle_kind_to_uf[MleKind(metal='M', entering='L', leaving='X')]
    assert sorted([sorted(group) for group in uf.to_sets()]) == [
        [MleBindsite('M1.b', 'X1.a', 'L1.b')],
    ]


def test_for_specific_assembly_with_aux_edges() -> None:
    MLX3 = Assembly(
        {'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X', 'X3': 'X'},
        {('M1.a', 'X1.a'), ('M1.b', 'X2.a'), ('M1.c', 'X3.a'), ('M1.d', 'L1.a')}
    )
    MLE_KINDS = [
        MleKind(metal='M', entering='L', leaving='X'),
    ]
    COMPONENT_STRUCTURES = {
        'M': Component(
            'M', {'a', 'b', 'c', 'd'},
            {LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('b', 'c', 'cis'),
             LocalAuxEdge('c', 'd', 'cis'), LocalAuxEdge('d', 'a', 'cis')}),
        'L': Component('L', {'a', 'b'}),
        'X': Component('X', {'a'})
    }
    mle_kind_to_uf = compute_mle_equivalence_as_uf(
        MLX3, MLE_KINDS, COMPONENT_STRUCTURES)
    
    assert mle_kind_to_uf.keys() == {MleKind(metal='M', entering='L', leaving='X')}

    uf = mle_kind_to_uf[MleKind(metal='M', entering='L', leaving='X')]
    assert sorted([sorted(group) for group in uf.to_sets()]) == [
        [  # cis exchanges
            MleBindsite('M1.a', 'X1.a', 'L1.b'),
            MleBindsite('M1.c', 'X3.a', 'L1.b'),
        ],
        [MleBindsite('M1.b', 'X2.a', 'L1.b')],  # trans exchange
    ]


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
