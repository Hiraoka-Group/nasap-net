from collections.abc import Iterable
from pathlib import Path

import yaml

from recsa import InterReaction, IntraReaction

__all__ = ['load_reaction']


def load_reaction(
        file_path: str | Path
        ) -> IntraReaction | InterReaction:
    file_path = Path(file_path)

    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)

    if data.get('entering_assem_id') is None:
        return IntraReaction(**data)
    else:
        return InterReaction(**data)
