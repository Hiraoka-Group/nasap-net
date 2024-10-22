from collections.abc import Iterator
from pathlib import Path
from typing import TypeAlias

import recsa as rx

from .assembly import load_assembly

__all__ = ['load_assemblies']


AssemblyId: TypeAlias = str

def load_assemblies(
        folder_path: str | Path
        ) -> Iterator[tuple[AssemblyId, rx.Assembly]]:
    """Load Assembly objects from a folder of YAML files.
    
    The file name (without the extension) is used as the assembly ID.
    """
    for file_path in Path(folder_path).iterdir():
        if file_path.suffix == '.yaml':
            assem_id = file_path.stem
            assembly = load_assembly(file_path)
            yield assem_id, assembly
