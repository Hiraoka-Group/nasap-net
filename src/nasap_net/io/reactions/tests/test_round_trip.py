from nasap_net.io import load_reactions, save_reactions
from nasap_net.models import Assembly, BindingSite, Bond, Component, Reaction


def test_round_trip(tmp_path):
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

    assemblies = [MX2, free_L, MLX, free_X]

    reactions = [
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
    save_reactions(reactions, output_file)

    loaded_reactions = load_reactions(
        output_file, assemblies,
        site_id_type='int'
    )

    assert len(loaded_reactions) == len(reactions)
    for original, loaded in zip(reactions, loaded_reactions):
        assert original == loaded
