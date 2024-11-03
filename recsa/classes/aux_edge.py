from typing import Any

import yaml

import recsa as rx
from recsa.utils import FrozenUnorderedPair

from .validations import (validate_name_of_aux_type,
                          validate_name_of_binding_site)

__all__ = ['AuxEdge']


class AuxEdge(yaml.YAMLObject):
    """An auxiliary edge between two binding sites. (Immutable)"""
    yaml_loader = yaml.SafeLoader
    yaml_dumper = yaml.Dumper
    yaml_tag = '!AuxEdge'
    yaml_flow_style = None

    def __init__(
            self, local_bindsite1: str, local_bindsite2: str, aux_kind: str):
        """Initialize an auxiliary edge.

        Note that the order of the binding sites does not matter,
        i.e., AuxEdge('a', 'b', 'cis') is the same as AuxEdge('b', 'a', 'cis').

        Parameters
        ----------
        bindsite1 : str
            The local id of the first binding site.
        bindsite2 : str
            The local id of the second binding site.
        aux_type : str
            The auxiliary type.

        Note
        ----
        The order of the binding sites does not matter.

        Raises
        ------
        rx.RecsaValueError
            If the two binding sites are the same.
        """
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
    
    def __lt__(self, other: 'AuxEdge') -> bool:
        return (sorted(self.bindsites), self.aux_kind) < (
            sorted(other.bindsites), other.aux_kind)
    
    def __repr__(self) -> str:
        return f'AuxEdge({self.local_bindsite1!r}, {self.local_bindsite2!r}, {self.aux_kind!r})'
    
    @classmethod
    def from_yaml(cls, loader, node):
        data = loader.construct_mapping(node, deep=True)
        return AuxEdge(
            data['bindsites'][0], data['bindsites'][1], data['aux_kind'])

    @classmethod
    def to_yaml(cls, dumper, data):
        return dumper.represent_mapping(
            cls.yaml_tag, {
            'bindsites': sorted(data.bindsites),
            'aux_kind': data.aux_kind},
            flow_style=cls.yaml_flow_style)
