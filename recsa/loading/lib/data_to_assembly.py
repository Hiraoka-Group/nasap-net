from collections.abc import Iterable, Mapping
from typing import NotRequired, TypedDict

from recsa import Assembly


class AssemblyData(TypedDict):
    name: NotRequired[str]
    comp_id_to_kind: Mapping[str, str]
    bonds: NotRequired[Iterable[Iterable[str]] | None]


def convert_data_to_assembly(data: AssemblyData) -> Assembly:
    """Convert data to an Assembly object."""
    return Assembly(
        comp_id_to_kind=data['comp_id_to_kind'],
        bonds=data.get('bonds'),
        name=data.get('name'),
        )
