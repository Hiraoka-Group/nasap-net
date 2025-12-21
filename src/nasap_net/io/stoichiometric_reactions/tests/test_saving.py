import os
import tempfile

import pandas as pd
import pytest

from nasap_net.io.stoichiometric_reactions.saving import \
    save_stoichiometric_reactions
from nasap_net.models.stoichiometric_reaction import StoichiometricReaction


@pytest.fixture
def sample_reactions():
    return [
        StoichiometricReaction('A', None, 'B', None, 1, 'r1'),
        StoichiometricReaction('C', 'D', 'E', 'F', 2, 'r2'),
    ]


def test_basic(sample_reactions):
    reactions = sample_reactions
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, 'test.csv')
        save_stoichiometric_reactions(reactions, file_path)
        df = pd.read_csv(file_path)
        # Check columns and values
        assert set(df.columns) == {
            'reactant1', 'reactant2',
            'product1', 'product2',
            'duplicate_count', 'id',
        }
        assert len(df) == 2
        assert df['reactant1'][0] == 'A'
        assert df['product1'][1] == 'E'
        assert df['duplicate_count'][1] == 2


def test_overwrite(sample_reactions):
    reactions = sample_reactions
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, 'test.csv')
        save_stoichiometric_reactions(reactions, file_path)
        # Should raise FileExistsError if overwrite=False and file exists
        with pytest.raises(FileExistsError):
            save_stoichiometric_reactions(reactions, file_path)
        # Should succeed if overwrite=True
        save_stoichiometric_reactions(reactions, file_path, overwrite=True)


def test_index(sample_reactions):
    reactions = sample_reactions
    with tempfile.TemporaryDirectory() as tmpdir:
        file_path = os.path.join(tmpdir, 'test.csv')
        save_stoichiometric_reactions(reactions, file_path, index=True)
        df = pd.read_csv(file_path)
        # Check if index column is present or index is set
        assert 'index' in df.columns or df.index.name == 'index' or df.index[0] == 0
