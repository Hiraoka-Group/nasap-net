from pathlib import Path

import yaml
from pydantic.dataclasses import dataclass

from recsa import AuxEdge, Component

__all__ = ['load_component_structures']


def load_component_structures(
        file_path: str | Path
        ) -> dict[str, Component]:
    """Load ComponentStructure objects from a YAML file."""
    file_path = Path(file_path)
    data = load_yaml(file_path)
    return create_component_structures_from_data(data)


@dataclass
class AuxEdgeData:
    bindsite1: str
    bindsite2: str
    kind: str


@dataclass
class ComponentStructureData:
    id: str
    bindsites: list[str]
    aux_edges: list[AuxEdgeData] | None = None


@dataclass
class ComponentStructuresData:
    component_structures: list[ComponentStructureData]


def load_yaml(file_path: str | Path) -> list[ComponentStructureData]:
    """Load YAML file and return the data as a dictionary."""
    with open(file_path, 'r') as file:
        data = yaml.safe_load(file)
    
    component_structures = []
    for component_structure in data['component_structures']:
        component_structures.append(
            ComponentStructureData(**component_structure))
    return component_structures


def create_component_structures_from_data(
        data: list[ComponentStructureData]
        ) -> dict[str, Component]:
    """Create ComponentStructure objects from a dictionary."""
    component_structures = {}
    for component_structure in data:
        bindsites = set(component_structure.bindsites)
        aux_edges = set()
        if component_structure.aux_edges:
            if component_structure.aux_edges:
                for aux_edge in component_structure.aux_edges:
                    bindsite1 = aux_edge.bindsite1
                    bindsite2 = aux_edge.bindsite2
                    kind = aux_edge.kind
                    aux_edges.add(AuxEdge(bindsite1, bindsite2, kind))
        component_structures[component_structure.id] = Component(
            component_structure.id, bindsites, aux_edges)
    return component_structures
