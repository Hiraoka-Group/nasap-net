import os
from pathlib import Path

import pandas as pd

from nasap_net import StoichiometricReaction
from .models import StoichiometricReactionRow


def load_stoichiometric_reactions(
        file_path: os.PathLike | str,
        *,
        has_index_column: bool = False,
) -> list[StoichiometricReaction]:
    """Load stoichiometric reactions from a CSV file and convert to
    StoichiometricReaction objects.
    """
    file_path = Path(file_path)
    if not file_path.exists():
        raise FileNotFoundError(f'File "{str(file_path)}" does not exist.')
    df = pd.read_csv(
        file_path,
        index_col=0 if has_index_column else None,
    )
    df = df.astype(object).where(pd.notnull(df), None)  # type: ignore[call-overload]
    rows = [StoichiometricReactionRow.from_dict(row) for row in df.to_dict(orient="records")]
    return [row.to_stoichiometric_reaction() for row in rows]
