from pathlib import Path

from recsa import save_bondsets

from .core import enum_bond_subsets
from .loading import load_bond_based_structure_data

__all__ = ['enum_bond_subsets_pipeline']


def enum_bond_subsets_pipeline(
        input_path: str | Path, output_path: str | Path, 
        overwrite: bool = False
        ) -> None:
    """Enumerate connected subsets of bonds excluding symmetry-equivalent ones.

    This function reads the input file, enumerates connected subsets of bonds
    excluding symmetry-equivalent ones, and saves the results to the output file.

    Each step is performed by the following functions:
    1. Parse the input file using `parse_file_for_enum_bond_subsets`.
    2. Enumerate connected subsets of bonds excluding symmetry-equivalent ones
       using `enum_bond_subsets`.
    3. Save the results to the output file using 
       `save_results_of_enum_bond_subsets`.

    See the documentation of each function for details.

    Parameters
    ----------
    input_path : str
        Path to the input file containing the parameters for fragment 
        enumeration. The file should be in the format described in the
        documentation. See documentation for details.
    output_path : str
        Path to the output file to save the results.
        If the file already exists, the user is asked whether to overwrite it.
    overwrite : bool, optional
        Whether to overwrite the output file if it already exists.
        If False and the output file already exists, the user is asked
        whether to overwrite it.

    See Also
    --------
    parse_file_for_enum_bond_subsets : Function to parse the input file.
    enum_bond_subsets : Core function for enumerating fragments.
    save_results_of_enum_bond_subsets : Function to save the results.
    """
    args = load_bond_based_structure_data(input_path)

    bondsets = enum_bond_subsets(
        bonds=args.bonds, 
        bond_to_adj_bonds=args.bond_to_adjs, 
        sym_ops=args.symmetry_ops)
    
    save_bondsets(
        bondsets, output_path, overwrite=overwrite)
