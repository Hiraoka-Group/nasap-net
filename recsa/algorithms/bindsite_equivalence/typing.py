from collections.abc import Mapping
from typing import TypeAlias

__all__ = ['BindsiteToRoot', 'RootToBindsites', 'AssemblyId', 'ComponentKind']


BindsiteToRoot: TypeAlias = Mapping[str, str]
RootToBindsites: TypeAlias = Mapping[str, set[str]]
AssemblyId: TypeAlias = str
ComponentKind: TypeAlias = str
