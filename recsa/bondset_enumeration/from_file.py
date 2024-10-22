from pathlib import Path

from .core import enum_bond_subsets
from .loading import load_bond_based_structure_data

__all__ = ['enum_bond_subsets_from_file']


def enum_bond_subsets_from_file(
        input_path: str | Path) -> set[frozenset[str]]:
    """Enumerate connected subsets of bonds excluding symmetry-equivalent ones.

    This function parses parameters from the input file using
    `parse_args_for_enum_bond_subsets`, and calls `enum_bond_subsets` 
    with the parsed parameters.

    For more details, see the documentation of `enum_bond_subsets`.

    Parameters
    ----------
    input_path : str
        Path to the input file containing the parameters for fragment 
        enumeration. The file should be in the format described in the
        documentation. See documentation for details.

    Returns
    -------
    set[frozenset[BondId]]
        A set of connected subsets of bonds excluding symmetry-equivalent
        ones. Each subset is represented as a frozenset of bond IDs.

    Notes
    -----
    - This function is a wrapper around `enum_bond_subsets` and 
    `parse_args_for_enum_bond_subsets`, combining file parsing 
    and enumeration in one step.
    - Bond IDs are read as strings from the input file.

    See Also
    --------
    parse_args_for_enum_bond_subsets : Function to parse the input file.
    enum_bond_subsets : Core function for enumerating fragments.
    """
    args = load_bond_based_structure_data(input_path)
    return enum_bond_subsets(
        bonds=args.bonds, 
        bond_to_adj_bonds=args.bond_to_adjs, 
        sym_ops=args.symmetry_ops)
