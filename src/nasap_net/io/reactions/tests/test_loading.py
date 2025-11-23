from nasap_net.io import load_reactions
from nasap_net.models import Assembly, BindingSite, Bond, Component, Reaction


def test_load_reactions_from_file(tmp_path):

    # Create assemblies to be used in reactions
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

    # Create a CSV file with reaction data
    reaction_data = """init_assem_id,entering_assem_id,product_assem_id,leaving_assem_id,metal_bs_component,metal_bs_site,leaving_bs_component,leaving_bs_site,entering_bs_component,entering_bs_site,duplicate_count
MX2,free_L,MLX,free_X,M0,0,X0,0,L0,0,4
"""
    reaction_file = tmp_path / 'reactions.csv'
    reaction_file.write_text(reaction_data)
    # Import reactions from the CSV file
    imported_reactions = load_reactions(
        reaction_file, assemblies,
        assembly_id_type='str',
        component_id_type='str',
        site_id_type='str',
    )
    # Define the expected reaction
    expected_reaction = Reaction(
        init_assem=MX2,
        entering_assem=free_L,
        product_assem=MLX,
        leaving_assem=free_X,
        metal_bs=BindingSite('M0', '0'),
        leaving_bs=BindingSite('X0', '0'),
        entering_bs=BindingSite('L0', '0'),
        duplicate_count=4,
    )
    # Assert that the imported reactions match the expected reaction
    assert len(imported_reactions) == 1
    assert imported_reactions[0] == expected_reaction
