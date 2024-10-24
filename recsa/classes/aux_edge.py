from typing import Any

import recsa as rx
from recsa.utils import FrozenUnorderedPair

from .validations import (validate_name_of_aux_type,
                          validate_name_of_binding_site)

__all__ = ['AuxEdge']


class AuxEdge:
    """An auxiliary edge between two binding sites. (Immutable)"""
    def __init__(
            self, local_bindsite1: str, local_bindsite2: str, aux_kind: str):
        validate_name_of_binding_site(local_bindsite1)
        validate_name_of_binding_site(local_bindsite2)
        if local_bindsite1 == local_bindsite2:
            raise rx.RecsaValueError(
                'The two binding sites should be different.')
        self._bindsites = FrozenUnorderedPair[str](
            local_bindsite1, local_bindsite2)

        validate_name_of_aux_type(aux_kind)
        self._aux_kind = aux_kind
    
    @property
    def local_bindsite1(self) -> str:
        return self._bindsites.first
    
    @property
    def local_bindsite2(self) -> str:
        return self._bindsites.second
    
    @property
    def bindsites(self) -> FrozenUnorderedPair[str]:
        return self._bindsites

    @property
    def aux_kind(self) -> str:
        return self._aux_kind

    def __hash__(self) -> int:
        return hash((self.bindsites, self.aux_kind))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AuxEdge):
            return False
        return (
            self.bindsites == other.bindsites and
            self.aux_kind == other.aux_kind)

    def __repr__(self) -> str:
        return (
            f'AuxEdge({self.local_bindsite1!r}, '
            f'{self.local_bindsite2!r}, {self.aux_kind!r})')
