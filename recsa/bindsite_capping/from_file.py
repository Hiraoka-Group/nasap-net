from collections.abc import Iterator
from pathlib import Path

from recsa import Assembly, load_assemblies, load_component_structures

from .loading import load_cap_args
from .multi_bindsites import cap_bindsites

__all__ = ['cap_bindsites_from_file']


def cap_bindsites_from_file(
        assemblies_dir: str | Path,
        component_structures_path: str | Path,
        cap_params_path: str | Path,
        ) -> Iterator[tuple[str, Assembly]]:
    """Cap bindsites for all assemblies."""
    id_assembly_pairs = load_assemblies(assemblies_dir)
    component_structures = load_component_structures(
        component_structures_path)
    cap_params = load_cap_args(cap_params_path)

    for id_, assembly in id_assembly_pairs:
        assembly = cap_bindsites(
            assembly, component_structures, 
            cap_params.component_kind_to_be_capped,
            cap_params.cap_component_kind, cap_params.cap_bindsite)
        yield id_, assembly
