from typing import TypeAlias

from nasap_net import IntraReaction, InterReaction

Reaction: TypeAlias = IntraReaction | InterReaction
