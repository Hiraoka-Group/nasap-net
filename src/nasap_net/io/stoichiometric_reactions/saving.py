import logging
import os
from collections.abc import Iterable
from pathlib import Path

import pandas as pd

from nasap_net import StoichiometricReaction
from .models import StoichiometricReactionRow

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def save_stoichiometric_reactions(
        reactions: Iterable[StoichiometricReaction],
        file_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        index: bool = False,
        ) -> None:
    """Save stoichiometric reactions to a CSV file.

    Columns: reactant1, reactant2, product1, product2, duplicate_count, id
    """
    file_path = Path(file_path)
    if file_path.exists() and not overwrite:
        raise FileExistsError(
            f'File "{str(file_path)}" already exists. '
            'Use `overwrite=True` to overwrite it.'
        )
    reactions = list(reactions)
    df = stoichiometric_reactions_to_df(reactions)
    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=index)
    logger.info('Saved %d stoichiometric reactions to "%s"', len(reactions), str(file_path))


def stoichiometric_reactions_to_df(reactions: Iterable[StoichiometricReaction]) -> pd.DataFrame:
    rows = [StoichiometricReactionRow.from_stoichiometric_reaction(r).to_dict() for r in reactions]
    return pd.DataFrame(rows)
