import logging
import os
from collections.abc import Mapping
from pathlib import Path

import pandas as pd

from nasap_net.models import Reaction
from ..reactions.models import ReactionRow

logger = logging.getLogger(__name__)
logger.addHandler(logging.NullHandler())


def save_classification_result(
        reaction_to_class: Mapping[Reaction, str],
        file_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        index: bool = False,
        ) -> None:
    """Save the classification result to a CSV file.

    Resulting CSV columns:
    - init_assem_id : str | int
    - entering_assem_id : str | int | None
    - product_assem_id : str | int
    - leaving_assem_id : str | int | None
    - metal_bs_component : str | int
    - metal_bs_site : str | int
    - leaving_bs_component : str | int
    - leaving_bs_site : str | int
    - entering_bs_component : str | int
    - entering_bs_site : str | int
    - duplicate_count : int
    - id : str | int | None
    - reaction_class : str

    Parameters
    ----------
    reaction_to_class : Mapping[Reaction, str]
        Mapping from Reaction objects to their corresponding class labels.
    file_path : os.PathLike | str
        Path to the CSV file to write.
    overwrite : bool, optional
        If True, overwrite the file if it already exists.
        If False, raise an error if the file already exists.
        Default is False.
    index : bool, optional
        If True, write row names (index). Default is False.
    """
    file_path = Path(file_path)
    if file_path.exists() and not overwrite:
        raise FileExistsError(
            f'File "{str(file_path)}" already exists. '
            'Use `overwrite=True` to overwrite it.'
        )

    df = classification_result_to_df(reaction_to_class)

    file_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(file_path, index=index)
    logger.info(
        'Saved %d reactions to "%s"',
        len(reaction_to_class),
        str(file_path)
    )


def classification_result_to_df(
        reaction_to_class: Mapping[Reaction, str]
) -> pd.DataFrame:
    """Convert an iterable of Reaction objects to a pandas DataFrame.

    Parameters
    ----------
    reaction_to_class : Mapping[Reaction, str]
        Mapping from Reaction objects to their corresponding class labels.

    Returns
    -------
    pd.DataFrame
        DataFrame representation of the reactions.

    Raises
    ------
    IDNotSetError
        If any assembly ID in the reactions is not set.
    """
    rows = [
        _rename_id_key(
            ReactionRow.from_reaction(reaction).to_dict()
            | {'reaction_class': reaction_class}
        )
        for reaction, reaction_class in reaction_to_class.items()
    ]

    return pd.DataFrame(rows)


def _rename_id_key(d: dict) -> dict:
    """Rename the 'id_' key in the dictionary to 'id'."""
    if 'id_' in d:
        d['id'] = d.pop('id_')
    return d
