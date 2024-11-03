from collections.abc import Iterable
from pathlib import Path
from typing import NotRequired, TypedDict

import yaml

from recsa import AuxEdge, Component
from recsa.utils import find_unique_filepath


def save_components(
        comp_kind_to_obj: dict[str, Component],
        output_path: str | Path,
        *,
        overwrite: bool = False) -> None:
    """Save components as a YAML file."""
    output_path = Path(output_path)

    if output_path.exists() and not overwrite:
        output_path = find_unique_filepath(output_path)
        assert not output_path.exists()
    
    with output_path.open('w') as f:
        yaml.dump(comp_kind_to_obj, f, default_flow_style=None)
