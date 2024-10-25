from pathlib import Path

import yaml
from pydantic import BaseModel, field_validator

from recsa import Assembly

from .component_structures import (ComponentStructureData,
                                   create_component_structures_from_data)

__all__ = ['load_assembly']


def load_assembly(file_path: str | Path) -> Assembly:
    """Load an Assembly object from a YAML file."""
    file_path = Path(file_path)
    data = load_yaml(file_path)
    return create_assembly_from_data(data)


class AssemblyData(BaseModel):
    component_structures: dict[str, ComponentStructureData]
    component_id_to_kind: dict[str, str]
    bonds: set[frozenset[str]] | None

    @field_validator('bonds')
    def validate_bonds(cls, value):
        return value or set()


def load_yaml(file_path: str | Path) -> AssemblyData:
    """Load YAML file and return the data as a dictionary."""
    file_path = Path(file_path)
    with file_path.open('r') as f:
        data = yaml.safe_load(f)
    return AssemblyData(**data)


def create_assembly_from_data(data: AssemblyData) -> Assembly:
    """Create an Assembly object from a dictionary."""
    comp_kind_to_structure = create_component_structures_from_data(
        list(data.component_structures.values()))
    return Assembly(
        comp_kind_to_structure, data.component_id_to_kind, 
        data.bonds)
