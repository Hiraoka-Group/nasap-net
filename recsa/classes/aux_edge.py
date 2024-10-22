from typing import Any

from recsa import RecsaValueError

from .validations import (validate_name_of_aux_type,
                          validate_name_of_binding_site)

__all__ = ['AuxEdge']


class AuxEdge:
    """An auxiliary edge between two binding sites."""
    def __init__(
            self, bindsite1: str, bindsite2: str, aux_kind: str):
        """Initialize an auxiliary edge.

        Note that the order of the binding sites does not matter,
        i.e., AuxEdge('a', 'b', 'cis') is the same as AuxEdge('b', 'a', 'cis').

        Parameters
        ----------
        bindsite1 : str
            The first binding site. 
        bindsite2 : str
            The second binding site. 
        aux_type : str
            The auxiliary type.

        Raises
        ------
        RecsaValueError
            If the two binding sites are the same.
        """
        validate_name_of_binding_site(bindsite1)
        validate_name_of_binding_site(bindsite2)
        if bindsite1 == bindsite2:
            raise RecsaValueError(
                'The two binding sites should be different.')
        self.bindsites = {bindsite1, bindsite2}

        validate_name_of_aux_type(aux_kind)
        self.aux_type = aux_kind
    
    @property
    def bindsite1(self) -> str:
        return sorted(self.bindsites)[0]
    
    @property
    def bindsite2(self) -> str:
        return sorted(self.bindsites)[1]

    def __hash__(self) -> int:
        return hash((tuple(sorted(self.bindsites)), self.aux_type))

    def __eq__(self, other: Any) -> bool:
        if not isinstance(other, AuxEdge):
            return False
        return (
            self.bindsites == other.bindsites and
            self.aux_type == other.aux_type)

    def __repr__(self) -> str:
        [first, second] = sorted(self.bindsites)
        return f'AuxEdge({first!r}, {second!r}, {self.aux_type!r})'
