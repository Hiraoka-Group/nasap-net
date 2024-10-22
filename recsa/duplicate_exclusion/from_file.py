from collections.abc import Iterator

from recsa import Assembly, load_assemblies, load_component_structures

from .core import find_unique_assemblies

__all__ = ['find_unique_assemblies_from_file']


def find_unique_assemblies_from_file(
        assemblies_input_folder: str,
        component_structures_path: str,
        ) -> Iterator[tuple[str, Assembly]]:
    """Exclude remaining duplicates"""
    assemblies = load_assemblies(assemblies_input_folder)
    component_structures = load_component_structures(
        component_structures_path)
    yield from find_unique_assemblies(assemblies, component_structures)
