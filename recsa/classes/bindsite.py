from __future__ import annotations

from copy import copy

from .bindsite_id_converter import BindsiteIdConverter
from .validations import validate_name_of_binding_site


class BindSite:
    """Binding site of a component. (Immutable)"""

    def __init__(
            self, local: str, comp_id: str | None = None) -> None:
        validate_name_of_binding_site(local)
        self._local = local
        self._comp_id = comp_id

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, BindSite):
            return False
        return self.local == other.local and self.comp_id == other.comp_id

    def __hash__(self) -> int:
        return hash((self.comp_id, self.local))

    @property
    def comp_id(self) -> str | None:
        return self._comp_id

    @property
    def local(self) -> str:
        return self._local

    @property
    def global_(self) -> str | None:
        id_converter = BindsiteIdConverter()
        if self._comp_id is None or self._local is None:
            return None
        return id_converter.local_to_global(self._comp_id, self._local)

    def with_comp_id(self, comp_id: str) -> BindSite:
        self_copy = copy(self)
        self_copy._comp_id = comp_id
        return self_copy

    @classmethod
    def from_global(cls, global_: str) -> BindSite:
        id_converter = BindsiteIdConverter()
        comp_id, local = id_converter.global_to_local(global_)
        return cls(local, comp_id)
