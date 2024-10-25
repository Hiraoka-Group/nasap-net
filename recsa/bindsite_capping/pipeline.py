import shutil
from pathlib import Path

from recsa import load_assemblies, load_component_structures, save_assembly
from recsa.utils import find_unique_filepath

from .loading import load_cap_args
from .multi_bindsites import cap_bindsites

__all__ = ['cap_bindsites_pipeline']


def cap_bindsites_pipeline(
        assemblies_dir: str | Path,
        component_structures_path: str | Path,
        cap_params_path: str | Path,
        output_dir: str | Path,
        overwrite: bool = False
        ) -> None:
    """Cap bindsites for all assemblies."""
    id_assembly_pairs = load_assemblies(assemblies_dir)
    component_structures = load_component_structures(
        component_structures_path)
    cap_params = load_cap_args(cap_params_path)

    output_dir = Path(output_dir)
    if output_dir.exists() and not output_dir.is_dir():
        raise ValueError('Output path should be a directory path.')
    if output_dir.exists():
        if overwrite:
            # Remove the existing folder together with its contents
            shutil.rmtree(output_dir)
        else:
            output_dir = find_unique_filepath(output_dir)
            assert not output_dir.exists()
    output_dir.mkdir(parents=True, exist_ok=True)

    for id_, assembly in id_assembly_pairs:
        assembly = cap_bindsites(
            assembly, component_structures, 
            cap_params.component_kind_to_be_capped,
            cap_params.cap_component_kind, cap_params.cap_bindsite)
        output_path = output_dir / f'{id_}.yaml'
        save_assembly(assembly, output_path, overwrite=False)
