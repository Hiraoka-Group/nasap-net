from itertools import tee
from pathlib import Path

from recsa import load_assemblies, load_component_structures, save_assemblies

from .core import find_unique_assemblies

__all__ = ['find_unique_assemblies_pipeline']


def find_unique_assemblies_pipeline(
        assemblies_input_folder: str | Path,
        component_structures_path: str | Path,
        output_dir: str | Path,
        overwrite: bool = False
        ) -> None:
    """Exclude remaining duplicates from assemblies."""
    id_assembly_pairs = load_assemblies(assemblies_input_folder)
    component_structures = load_component_structures(
        component_structures_path)
    unique_id_assembly_pairs = find_unique_assemblies(
        id_assembly_pairs, component_structures)
    
    # Use tee to iterate over the pairs twice
    paris1, pairs2 = tee(unique_id_assembly_pairs)
    ids = (id_ for id_, _ in paris1)
    assemblies = (assembly for _, assembly in pairs2)
    
    save_assemblies(
        assemblies, output_dir, overwrite=overwrite)
