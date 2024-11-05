import pytest

from recsa import InterReaction, IntraReaction, reactions_to_df


def test_basic():
    reactions: list[IntraReaction | InterReaction] = [
        IntraReaction(
            'init1', 'prod1', 'leave1', 
            'metal_bs1', 'leave_bs1', 'enter_bs1', 
            'metal_kind1', 'leave_kind1', 'enter_kind1', 1),
        InterReaction(
            'init2', 'enter2', 'prod2', 'leave2',
            'metal_bs2', 'leave_bs2', 'enter_bs2',
            'metal_kind2', 'leave_kind2', 'enter_kind2', 2)
    ]

    df = reactions_to_df(reactions)

    assert df.shape == (2, 11)
    assert df.columns.tolist() == [
        'init_assem_id', 'entering_assem_id', 'product_assem_id',
        'leaving_assem_id', 'metal_bs', 'leaving_bs', 'entering_bs',
        'metal_kind', 'leaving_kind', 'entering_kind', 'duplicate_count'
    ]
    assert df['init_assem_id'].tolist() == ['init1', 'init2']
    assert df['entering_assem_id'].tolist() == [None, 'enter2']
    assert df['product_assem_id'].tolist() == ['prod1', 'prod2']
    assert df['leaving_assem_id'].tolist() == ['leave1', 'leave2']
    assert df['metal_bs'].tolist() == ['metal_bs1', 'metal_bs2']
    assert df['leaving_bs'].tolist() == ['leave_bs1', 'leave_bs2']
    assert df['entering_bs'].tolist() == ['enter_bs1', 'enter_bs2']
    assert df['metal_kind'].tolist() == ['metal_kind1', 'metal_kind2']
    assert df['leaving_kind'].tolist() == ['leave_kind1', 'leave_kind2']
    assert df['entering_kind'].tolist() == ['enter_kind1', 'enter_kind2']
    assert df['duplicate_count'].tolist() == [1, 2]


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
