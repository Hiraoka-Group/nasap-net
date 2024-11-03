from recsa import (load_bondsets, load_structure_data,
                   save_assemblies_to_single_file)

from .multiple_assemblies import convert_bondsets_to_assemblies

__all__ = ['convert_bondsets_to_assemblies_pipeline']


def convert_bondsets_to_assemblies_pipeline(
        bondsets_path: str, structure_path: str,
        output_dir: str, overwrite: bool = False
        ) -> None:
    """Translate bond subsets to assembly objects and save them to a file."""
    id_to_bondset = load_bondsets(bondsets_path)
    args = load_structure_data(structure_path)

    assemblies = convert_bondsets_to_assemblies(
        bondsets=[frozenset(bondset) for bondset in id_to_bondset.values()],
        components=args.components,
        bond_id_to_bindsites=args.bond_id_to_bindsites,
    )

    save_assemblies_to_single_file(assemblies, output_dir, overwrite=overwrite)
