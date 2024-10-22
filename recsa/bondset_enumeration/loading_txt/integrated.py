import warnings
from pathlib import Path

from recsa import RecsaParsingError
from recsa.utils import parse_sections

from ..validation import validate_symmetry_ops_consistency
from .adj_bonds import parse_adj_bonds
from .bonds import parse_bonds
from .symmetry_cyclic_perms import parse_symmetry_cyclic_perms
from .symmetry_maps import parse_symmetry_maps

__all__ = ['load_args_for_enum_bond_subsets']


def load_args_for_enum_bond_subsets(
        filepath: str
        ) -> tuple[set[str], dict[str, set[str]], dict[str, dict[str, str]]]:
    """Parse the input file for `enum_bond_subsets`.

    Reads the input file and parses the sections for bond adjacency 
    and symmetry operations, which are required for `enum_bond_subsets`
    function as parameters.

    Required sections:
    - [bonds]: A comma-separated list of bond names.
    - [adj]: Adjacency list of bonds.
    - Either [map] or [cyclic]: Symmetry operations.

    For more details on the format of the input file, see the documentation

    Parameters
    ----------
    filepath : str
        Path to the input file.

    Returns
    -------
    bonds : set[str]
        A set of bond names. Each bond ID is a string.
    bond_to_adj_bonds : dict[str, set[str]]
        A dictionary mapping a bond to its adjacent bonds.
        Each key is the ID of a bond, and its value is a set of IDs
        of adjacent bonds.
    symmetry_ops : dict[str, dict[str, str]]
        A dictionary of symmetry operations.
        Each key is the name of a symmetry operation, and its value is
        a mapping of bond IDs to their images under the symmetry operation.
    
    Raises
    ------
    RecsaParsingError
        If the input file is not in the correct format.
        e.g., missing sections, invalid bond names, etc.
    RecsaMapCyclicInconsistencyError
        If both [map] and [cyclic] sections are present and inconsistent.

    Warnings
    --------
    If there are unknown sections in the input file, they are ignored,
    and a warning is issued.

    See Also
    --------
    enum_bond_subsets : Enumerate connected subsets of bonds excluding 
        symmetry-equivalent ones.

    Examples
    --------
    # TODO: Add examples
    """
    text = Path(filepath).read_text()

    # `sections` is a dictionary of sections in the input file.
    # The key is the section name, and the value is the lines 
    # (i.e. list of strings) in the section.
    sections = parse_sections(text)

    # 'bonds' section is required.
    if 'bonds' not in sections:
        raise RecsaParsingError('Missing [bonds] section.')

    # 'adj' section is required.
    if 'adj' not in sections:
        raise RecsaParsingError('Missing [adj] section.')
    
    # Either 'map' or 'cyclic' section is required.
    if 'map' not in sections and 'cyclic' not in sections:
        raise RecsaParsingError(
            'Neither [map] nor [cyclic] section is present.')
    
    # If there are other sections, warn the user, and ignore them.
    if sections.keys() - {'bonds', 'adj', 'map', 'cyclic'}:
        warnings.warn(
            'Ignoring unknown sections: ' +
            ', '.join(sections.keys() - {'bonds', 'adj', 'map', 'cyclic'}))
    
    # Parse the 'bonds' section. (Validation included)
    bonds = parse_bonds(sections['bonds'])
    
    # Parse the 'adj' section. (Validation included)
    bond_to_adj_bonds = parse_adj_bonds(sections['adj'], bonds)

    # Parse the symmetry operations. (Validation included)
    if 'map' in sections:
        ops_by_map = parse_symmetry_maps(sections['map'], bonds)
    if 'cyclic' in sections:
        ops_by_perms = parse_symmetry_cyclic_perms(
            sections['cyclic'], bonds)
    
    # Check the consistency if both 'map' and 'cyclic' sections are present.
    if 'map' in sections and 'cyclic' in sections:
        validate_symmetry_ops_consistency(ops_by_map, ops_by_perms)
        symmetry_ops = ops_by_map
    elif 'map' in sections:
        symmetry_ops = ops_by_map
    elif 'cyclic' in sections:
        symmetry_ops = ops_by_perms
    
    return bonds, bond_to_adj_bonds, symmetry_ops
