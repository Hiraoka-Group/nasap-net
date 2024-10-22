from pathlib import Path

from .formatting import format_bond_subsets

__all__ = ['save_bondsets_as_txt']


def save_bondsets_as_txt(
        output_path: str | Path, bond_subsets: set[frozenset[str]],
        overwrite: bool = False
        ) -> None:
    """Save the results of `enum_bond_subsets` to a file.

    The results are saved in the format described in the documentation.

    Parameters
    ----------
    output_path : str
        Path to the output file to save the results.
        If the file already exists, the user is asked whether to 
        overwrite it.
    bond_subsets : set[frozenset[str]]
        A set of bond subsets.
        Each bond subset is a frozenset of bond IDs.
    overwrite : bool, optional
        Whether to overwrite the output file if it already exists.
        If False and the output file already exists, the user is asked
        whether to overwrite it.
    """
    output_path = Path(output_path)
    
    if output_path.exists() and not output_path.is_file():
        raise ValueError('Output path should be a file path.')
    
    if output_path.exists() and not overwrite:
        if input('Output file already exists. Overwrite? (y/n): ') != 'y':
            print('Canceled.')
            return

    output_dir = output_path.parent
    output_dir.mkdir(parents=True, exist_ok=True)

    with output_path.open('w') as f:
        for line in format_bond_subsets(bond_subsets):
            f.write(line + '\n')

    print(f'Saved! ---> "{output_path}"')
