from collections.abc import Iterable
from typing import TypeAlias

import pandas as pd

from recsa import InterReaction, IntraReaction

Reaction: TypeAlias = IntraReaction | InterReaction


def reactions_to_df(reactions: Iterable[Reaction]) -> pd.DataFrame:
    return pd.DataFrame([reaction.to_dict() for reaction in reactions])
