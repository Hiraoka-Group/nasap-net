from pathlib import Path
from typing import Any

from recsa import AuxEdge, Component

from .yaml_safe_load import load_yaml_safely

__all__ = ['load_component_structures']


def load_component_structures(
        file_path: str | Path) -> dict[str, Component]:
    """Load ComponentStructure objects from a YAML file."""
    file_path = Path(file_path)
    data = load_yaml_safely(file_path)
    return create_component_structures_from_data(data)


def create_component_structures_from_data(
        data: Any) -> dict[str, Component]:
    """Create ComponentStructure objects from a dictionary."""
    # Expected format:
    # {'components': {
    #     'M': {
    #         'bindsites': ['a', 'b'],
    #         'aux_edges': [['a', 'b', 'cis']]
    #     },
    #     'X': {
    #         'bindsites': ['a'],
    #     }
    # }}

    if not isinstance(data, dict):
        raise ValueError('Expected a dictionary')
    if 'components' not in data:
        raise ValueError('Expected a key "component_structures"')
    
    comp_kind_to_data = data['components']
    if not isinstance(comp_kind_to_data, dict):
        raise ValueError('Expected a dictionary')
    
    comp_kind_to_obj = {}

    for comp_kind, comp_data in comp_kind_to_data.items():
        bindsites_data = comp_data.get('bindsites', [])
        bindsites_data = [str(bind) for bind in bindsites_data]

        aux_edges_data = comp_data.get('aux_edges', [])
        aux_edges_data = [
            AuxEdge(*aux_param) for aux_param in aux_edges_data]
        
        comp_kind_to_obj[comp_kind] = Component(
            bindsites=bindsites_data,
            aux_edges=aux_edges_data
        )
    
    return comp_kind_to_obj
