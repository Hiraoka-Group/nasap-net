from pathlib import Path

import yaml

from recsa import save_assemblies
from recsa.utils import find_unique_filepath

from .loading import CapParams
from .multi_assemblies import cap_bindsites_for_multi_assemblies

__all__ = ['cap_bindsites_pipeline']


def cap_bindsites_pipeline(
        assemblies_path: str | Path,
        comp_structure_path: str | Path,
        cap_params_path: str | Path,
        output_path: str | Path,
        *,
        overwrite: bool = False,
        show_progress: bool = True,
        save_with_index: bool = True,
        ) -> None:
    """Cap bindsites for all assemblies."""
    with open(assemblies_path) as f:
        assemblies_with_data = list(yaml.safe_load_all(f))
    with open(comp_structure_path) as f:
        components = yaml.safe_load(f)
    with open(cap_params_path) as f:
        cap_params_d = yaml.safe_load(f)
    cap_params = CapParams(**cap_params_d)

    output_path = Path(output_path)
    if output_path.exists() and not overwrite:
        output_path = find_unique_filepath(output_path)
        assert not output_path.exists()

    assemblies = (x['assembly'] for x in assemblies_with_data)
    capped_assemblies = cap_bindsites_for_multi_assemblies(
        assemblies, components, cap_params)
    
    save_assemblies(
        capped_assemblies, output_path, overwrite=overwrite,
        show_progress=show_progress, with_index=save_with_index)
