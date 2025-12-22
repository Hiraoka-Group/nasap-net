import pytest

from nasap_net.io import load_stoichiometric_reactions, \
    save_stoichiometric_reactions
from nasap_net.models.stoichiometric_reaction import StoichiometricReaction


@pytest.fixture
def reactions():
    return [
        StoichiometricReaction('A', 'B', 'C', None, 1, id_='R1'),
        StoichiometricReaction('X', None, 'Y', 'Z', 2, id_='R2'),
        StoichiometricReaction('M', None, 'N', None, 3, id_=None),
    ]


def test_round_trip(tmp_path, reactions):
    file = tmp_path / 'stoich_reactions.csv'
    save_stoichiometric_reactions(reactions, file)
    loaded = load_stoichiometric_reactions(file)
    assert len(loaded) == len(reactions)
    for r, l in zip(reactions, loaded):
        assert r == l


def test_with_index(tmp_path, reactions):
    file = tmp_path / 'stoich_reactions_with_index.csv'
    save_stoichiometric_reactions(reactions, file, index=True)
    loaded = load_stoichiometric_reactions(file, has_index_column=True)
    assert len(loaded) == len(reactions)
    for r, l in zip(reactions, loaded):
        assert r == l


def test_with_missing_id(tmp_path):
    reactions = [StoichiometricReaction('A', None, 'B', None, 1, id_=None)]
    file = tmp_path / 'stoich_reactions_no_id.csv'
    save_stoichiometric_reactions(reactions, file)
    loaded = load_stoichiometric_reactions(file)
    assert loaded[0].id_or_none is None
