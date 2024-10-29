import sys
from collections.abc import Callable, Iterable
from itertools import count
from pathlib import Path

import yaml

from recsa import Assembly

from .representers import add_assembly_representer

__all__ = ['save_assemblies_to_single_file']


add_assembly_representer()


def save_assemblies_to_single_file(
        assemblies: Iterable[Assembly],
        output_file: str | Path,
        *,
        overwrite: bool = False,
        show_progress: bool = True) -> None:
    """Save assemblies to a single YAML file."""
    output_file = Path(output_file)

    if output_file.exists() and not overwrite:
        raise FileExistsError(
            'Output file already exists and overwrite is set to False.')

    output_file.parent.mkdir(parents=True, exist_ok=True)

    with open(output_file, 'w') as f:
        first = True
        for index, assembly in enumerate(assemblies):
            if not first:
                f.write('---\n')  # YAML document separator
            yaml.dump(assembly, f)
            first = False
            if show_progress:
                # Update progress on the same line
                sys.stdout.write(f'\rSaving assembly {index + 1}...')
                sys.stdout.flush()

    if show_progress:
        # Print a new line after the loop is done
        print('\nAll assemblies saved successfully.')
