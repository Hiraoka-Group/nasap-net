from pathlib import Path
from typing import Any

import yaml

import recsa as rx


def load_yaml_safely(file_path: str | Path) -> Any:
    """Load a YAML file safely.
    
    Parameters
    ----------
    file_path : str or Path
        The path to the YAML file.

    Returns
    -------
    Any
        The data from the file.

    Raises
    ------
    RecsaLoadingError
        If the file does not contain valid YAML data.
    """
    file_path = Path(file_path)
    with file_path.open('r') as f:
        try:
            data = yaml.safe_load(f)
        except yaml.YAMLError as e:
            raise rx.RecsaLoadingError(
                f'Invalid YAML file: {file_path}') from e
    return data
