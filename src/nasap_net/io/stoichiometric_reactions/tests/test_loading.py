import pandas as pd
import pytest

from nasap_net import StoichiometricReaction
from nasap_net.io import load_stoichiometric_reactions


@pytest.fixture
def expected_reactions():
    return [
        StoichiometricReaction('A', None, 'B', None, 1, 'r1'),
        StoichiometricReaction('C', 'D', 'E', 'F', 2, 'r2'),
    ]


def test_load_from_expected_csv(tmp_path, expected_reactions):
    file_path = tmp_path / 'test.csv'
    df = pd.DataFrame([
        {'reactant1': 'A', 'reactant2': None, 'product1': 'B', 'product2': None, 'duplicate_count': 1, 'id': 'r1'},
        {'reactant1': 'C', 'reactant2': 'D', 'product1': 'E', 'product2': 'F', 'duplicate_count': 2, 'id': 'r2'},
    ])
    df.to_csv(file_path, index=False)
    loaded = load_stoichiometric_reactions(file_path)
    assert loaded == expected_reactions


def test_load_from_expected_csv_with_index(tmp_path, expected_reactions):
    file_path = tmp_path / 'test_with_index.csv'
    df = pd.DataFrame([
        {'reactant1': 'A', 'reactant2': None, 'product1': 'B', 'product2': None, 'duplicate_count': 1, 'id': 'r1'},
        {'reactant1': 'C', 'reactant2': 'D', 'product1': 'E', 'product2': 'F', 'duplicate_count': 2, 'id': 'r2'},
    ])
    df.to_csv(file_path, index=True)
    loaded = load_stoichiometric_reactions(file_path, has_index_column=True)
    assert loaded == expected_reactions
