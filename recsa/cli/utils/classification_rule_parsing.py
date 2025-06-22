from __future__ import annotations

import os
from collections.abc import Callable, Mapping, Sequence
from pathlib import Path
from typing import Any, Literal, Optional, TypeAlias, TypedDict

import yaml

from recsa import InterReaction, IntraReaction


def parse_classification_rule(
        path: os.PathLike | str
        ) -> Callable[[IntraReaction | InterReaction], int | str]:
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(
            f"Classification rule file {path} does not exist.")
    if not path.is_file():
        raise IsADirectoryError(
            f"Classification rule file {path} is not a file.")
    if path.suffix != ".yaml":
        raise ValueError(
            f"Classification rule file {path} is not a YAML file.")
    with open(path, "r") as file:
        try:
            rule = yaml.safe_load(file)
        except yaml.YAMLError as e:
            raise ValueError(f"Error parsing YAML file {path}: {e}")
    

    raise NotImplementedError()



ConditionKeyWord: TypeAlias = Literal[
    'AND', 'OR', 'NOT', 
    'ID', 'NAME', 'REV', 'COUNT', 'METAL_KIND', 'LEAVING_KIND', 'ENTERING_KIND',
    'REACTION_TYPE'
]
KeyWord: TypeAlias = ConditionKeyWord | Literal['IFS', 'IF', 'THEN', 'ELSE', 'RETURN']

Eval: TypeAlias = 'IfsBlock' | 'IfBlock' | 'ReturnBlock'

IdParams = TypedDict('IdParams', {'OF': str, 'IS': str})
NameParams = TypedDict('NameParams', {'OF': str, 'IS': str})
CountParams = TypedDict('CountParams', {'OF': str, 'IN': str, 'IS': int})

Condition: TypeAlias = (
    tuple[Literal['AND'], Sequence['Condition']] |
    tuple[Literal['OR'], Sequence['Condition']] |
    tuple[Literal['NOT'], 'Condition'] |
    tuple[Literal['NAME'], NameParams] |
    tuple[Literal['REV'], 'Condition'] |
    tuple[Literal['COUNT'], CountParams] |
    tuple[Literal['METAL_KIND'], str] | 
    tuple[Literal['LEAVING_KIND'], str] |
    tuple[Literal['ENTERING_KIND'], str] |
    tuple[Literal['REACTION_TYPE'], Literal['intra', 'inter']]
)

IfParams = TypedDict(
    'IfParams',
    {
        'IF': Condition,
        'THEN': Eval,
        'ELSE': Optional[Eval]
    }
)

IfBlock: TypeAlias = tuple[Literal['IF'], IfParams]
IfsBlock: TypeAlias = tuple[Literal['IFS'], Sequence[IfBlock]]
ThenBlock: TypeAlias = tuple[Literal['THEN'], Eval]
ElseBlock: TypeAlias = tuple[Literal['ELSE'], Eval]
ReturnBlock: TypeAlias = tuple[Literal['RETURN'], str | int]


def read_rule(rule: Any) -> Callable[[IntraReaction | InterReaction], int | str]:
    raise NotImplementedError()
    