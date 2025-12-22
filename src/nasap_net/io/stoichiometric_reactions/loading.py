import logging
import os
from pathlib import Path
from typing import Literal

import pandas as pd

from nasap_net.models import StoichiometricReaction
from .models import StoichiometricReactionRow

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def load_stoichiometric_reactions(
        file_path: os.PathLike | str,
        *,
        assembly_id_type: Literal['str', 'int'] = 'str',
        reaction_id_type: Literal['str', 'int'] = 'str',
        has_index_column: bool = False,
) -> list[StoichiometricReaction]:
    """Load reactions from a CSV file and convert to StoichiometricReaction objects."""
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f'File "{str(file_path)}" does not exist.')

    df = pd.read_csv(
        file_path,
        index_col=0 if has_index_column else None,
    )
    df = df.astype(object).where(pd.notnull(df), None)  # type: ignore[call-overload]

    types = {'int': int, 'str': str}

    reaction_rows = [
        StoichiometricReactionRow.from_dict(
            row,
            assembly_id_type=types[assembly_id_type],
            reaction_id_type=types[reaction_id_type],
        )
        for row in df.to_dict(orient="records")
    ]

    reactions = [
        stoich_reaction_row_to_stoich_reaction(reaction_row)
        for reaction_row in reaction_rows
    ]

    logger.info('Loaded %d StoichiometricReaction list from "%s"', len(reactions), str(file_path))

    return reactions


def stoich_reaction_row_to_stoich_reaction(
        stoich_reaction_row: StoichiometricReactionRow,
) -> StoichiometricReaction:
    """Convert a StoichiometricReactionRow to a Reaction object."""
    return StoichiometricReaction(
        reactant1=stoich_reaction_row.reactant1,
        reactant2=stoich_reaction_row.reactant2,
        product1=stoich_reaction_row.product1,
        product2=stoich_reaction_row.product2,
        duplicate_count=stoich_reaction_row.duplicate_count,
        id_=stoich_reaction_row.id_,
    )
