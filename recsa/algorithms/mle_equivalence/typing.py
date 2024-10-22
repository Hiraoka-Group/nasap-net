from collections.abc import Mapping
from typing import TypeAlias

from recsa import MleBindsite

__all__ = ['MleToRoot', 'RootToMles', 'AssemblyId']


AssemblyId: TypeAlias = str
MleToRoot: TypeAlias = Mapping[MleBindsite, MleBindsite]
RootToMles: TypeAlias = Mapping[MleBindsite, set[MleBindsite]]
