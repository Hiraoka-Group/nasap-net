import importlib.util
import os
from pathlib import Path
from types import ModuleType
from typing import Callable, Union


def import_classify_func(path: Union[os.PathLike, str]) -> Callable:
    """
    Imports a classification function from a Python file.
    The file must define a function named `classify` that takes a reaction
    object as an argument and returns a classification result.
    """
    module = _load_module_from_file(path)

    if not hasattr(module, "classify"):
        raise AttributeError("The rule file must define a 'classify' function")

    classify_func = getattr(module, "classify")
    return classify_func


def _load_module_from_file(path: Union[os.PathLike, str]) -> ModuleType:
    """
    Loads a Python module from a given file path.
    """
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"File not found: {path}")
    module_name = path.stem

    # Create a module spec from the file location
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None:
        raise ImportError(f"Could not load spec from {path}")
    
    # Create a new module based on the spec
    module = importlib.util.module_from_spec(spec)

    # Get the loader from the spec
    loader = spec.loader
    if loader is None:
        raise ImportError(f"No loader for spec from {path}")
    
    # Execute the module in its own namespace
    loader.exec_module(module)
    return module
