import pandas as pd

from nasap_net.io import export_reactions_to_file
from nasap_net.models import Assembly, BindingSite, Bond, Component, Reaction


def test_export_reactions_to_file(tmp_path):
    M = Component(kind='M', sites=[0, 1])
    L = Component(kind='L', sites=[0, 1])
    X = Component(kind='X', sites=[0])
    MX2 = Assembly(
        id_='MX2',
        components={'X0': X, 'M0': M, 'X1': X},
        bonds=[Bond('X0', 0, 'M0', 0), Bond('M0', 1, 'X1', 0)]
    )
    free_L = Assembly(id_='free_L', components={'L0': L}, bonds=[])
    MLX = Assembly(
        id_='MLX',
        components={'X0': X, 'M0': M, 'L0': L},
        bonds=[],
    )
    free_X = Assembly(id_='free_X', components={'X0': X}, bonds=[])

    reactions  = [
        Reaction(
            init_assem=MX2,
            entering_assem=free_L,
            product_assem=MLX,
            leaving_assem=free_X,
            metal_bs=BindingSite('M0', 0),
            leaving_bs=BindingSite('X0', 0),
            entering_bs=BindingSite('L0', 0),
            duplicate_count=4,
        )
    ]

    output_file = tmp_path / 'reactions.csv'
    export_reactions_to_file(reactions, output_file)

    assert output_file.exists()
    df = pd.read_csv(output_file)
    assert len(df) == 1
    row = df.iloc[0]
    assert row['init_assem_id'] == 'MX2'
    assert row['entering_assem_id'] == 'free_L'
    assert row['product_assem_id'] == 'MLX'
    assert row['leaving_assem_id'] == 'free_X'
    assert row['metal_bs_component'] == 'M0'
    assert row['metal_bs_site'] == 0
    assert row['leaving_bs_component'] == 'X0'
    assert row['leaving_bs_site'] == 0
    assert row['entering_bs_component'] == 'L0'
    assert row['entering_bs_site'] == 0
    assert row['duplicate_count'] == 4
