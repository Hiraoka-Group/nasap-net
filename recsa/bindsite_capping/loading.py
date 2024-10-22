from pathlib import Path

import yaml
from pydantic.dataclasses import dataclass

__all__ = ['CapParams', 'load_cap_args']


@dataclass
class CapParams:
    component_kind_to_be_capped: str
    cap_component_kind: str
    cap_bindsite: str


def load_cap_args(cap_params_path: str | Path) -> CapParams:
    """Load cap parameters from file."""
    with open(cap_params_path, 'r') as file:
        data = yaml.safe_load(file)
    return CapParams(**data)
