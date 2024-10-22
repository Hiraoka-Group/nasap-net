from collections.abc import Iterable
from dataclasses import dataclass
from typing import NewType

import yaml
from yaml.resolver import BaseResolver

__all__ = ['add_bondsets_representer', 'bondsets_representer', 'BondSets']

@dataclass(frozen=True)
class BondSets:
    bondsets: Iterable[Iterable[str]]


def bondsets_representer(dumper, data: BondSets):
    formatted = sorted(
        (sorted(bondset) for bondset in data.bondsets),
        key=lambda x: (len(x), x))
    return dumper.represent_sequence(BaseResolver.DEFAULT_SEQUENCE_TAG, formatted)


def add_bondsets_representer():
    yaml.add_representer(BondSets, bondsets_representer)
