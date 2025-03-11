import os
from collections.abc import Hashable, Iterable, Mapping
from typing import TypeVar

from recsa import enum_bond_subsets
from recsa.pipelines.lib import read_file, write_output
from recsa.utils import cyclic_perms_to_map

_T = TypeVar('_T', bound=Hashable)



# ============================================================
# Main Process
# ============================================================

def enum_bond_subsets_pipeline(
        input_path: os.PathLike | str,
        output_path: os.PathLike | str,
        *,
        overwrite: bool = False,
        verbose: bool = False
        ) -> None:
    """Enumerate bond subsets and save the result to a file.

    This function is a pipeline function that reads an input file,
    enumerates connected subsets of bonds excluding symmetry-equivalent
    ones, and saves the result to an output file.

    The core function that enumerates bond subsets is 
    `recsa.enum_bond_subsets`.

    See "Notes" section for details on the enumeration logic.

    Parameters
    ----------
    input_path : os.PathLike or str
        Path to the input file.
    output_path : os.PathLike or str
        Path to the output file.
    overwrite : bool, optional
        If True, overwrite the output file if it exists. Default is False.
    verbose : bool, optional
        If True, print detailed execution messages. Default is False.

    See Also
    --------
    recsa.enum_bond_subsets :
        The core function that enumerates bond subsets. 
        This function performs the actual enumeration logic, 
        while `enum_bond_subsets_pipeline` handles file I/O.

    Notes
    -----
    Functionality:
        When an assembly is represented as a set of bonds, subsets of 
        the bonds can be considered as fragments of the assembly.
        Considering the M2L3 linear assembly, L-M-L-M-L, with bonds named
        1, 2, 3, and 4 from left to right, for example, the assembly is 
        represented as {1, 2, 3, 4}, and its subsets such as {1}, {1, 2}, 
        and {2, 3} can be considered as fragments of the assembly, i.e.,
        L-M, L-M-L, and M-L-M, respectively.
        
        In this function, such subsets of bonds are enumerated
        under the following conditions:

        - Only connected subsets are enumerated.
        In the previous example, {1, 3} is not considered as a fragment.

        - Symmetry-equivalent fragments are excluded.
        If two fragments are superimposable under at least one symmetry 
        operation provided as `sym_ops`, only one of them is included 
        in the result.
        In the previous example, {1, 2} and {3, 4} are symmetry-equivalent
        under the C2 operation, thus only one of them is included in the
        result.

        Note that the result includes the assembly itself as a fragment,
        i.e., {1, 2, 3, 4} in the previous example.

        In summary, this function enumerates *connected* subsets of bonds
        *excluding symmetry-equivalent ones*.
    
    Style of Input File:
        The input file should be in YAML format.
        The required keys are as follows:
        - "bonds": A list of bond IDs.
        - "bond_adjacency": A dictionary mapping a bond to its adjacent bonds.
        - "sym_ops_by_bond_maps" or "sym_ops_by_bond_perms": A dictionary of symmetry operations 
        (Optional). Keys are the names of the symmetry operations. If 
        "sym_ops_by_bond_maps" is provided, the values are dictionaries mapping bond
        IDs to their images under the symmetry operation. If "sym_ops_by_bond_perms"
        is provided, the values are lists of cyclic permutations of bond
        IDs. If both are provided, "sym_ops_by_bond_maps" is used. If neither is
        provided, no symmetry-equivalence check is performed.
    
    Example of Input File::

        bonds: [1, 2, 3, 4]
        bond_adjacency:
            1: [2]
            2: [1, 3]
            3: [2, 4]
            4: [3]
        sym_ops_by_bond_maps:
            C2: {1: 4, 2: 3, 3: 2, 4: 1}
        sym_ops_by_bond_perms:
            C2: [[1, 4], [2, 3]]

    Style of Output File:
        The output file will be a dictionary with integer keys 
        starting from 0. Each key maps to a list of bond IDs representing 
        a connected subset of bonds. The subsets are sorted in a consistent 
        order based on the length of each subset and the elements within 
        each subset.
    
    Example of Output File::
    
        0: [1]
        1: [2]
        2: [1, 2]
        3: [2, 3]
        4: [1, 2, 3]
        5: [1, 2, 3, 4]
    """
    # Input
    input_data = read_file(input_path, verbose=verbose)
    validate_bonds(input_data['bonds'])
    validate_bond_adjacency(input_data['bond_adjacency'], input_data['bonds'])
    sym_ops = parse_sym_ops(input_data)
    if sym_ops is not None:
        validate_sym_ops(sym_ops, input_data['bonds'])
    
    # Main process
    if verbose:
        print('Enumerating bond subsets...')
    result = enum_bond_subsets(
        input_data['bonds'],
        input_data['bond_adjacency'],
        sym_ops)
    if verbose:
        print('Finished enumeration.')
        print(f'Number of bond subsets: {len(result)}')
    
    # Output
    formatted_result = sort_bond_subsets(result)

    id_to_bondset = {
        id_: bondset for id_, bondset in enumerate(formatted_result)
        }
    
    write_output(
        output_path, id_to_bondset, overwrite=overwrite, verbose=verbose,
        header='Enumerated bond subsets')


# ============================================================
# Input Processing
# ============================================================

def validate_bonds(bonds: list) -> None:
    if len(bonds) != len(set(bonds)):
        raise ValueError('"bonds" must not contain duplicates.')


def validate_bond_adjacency(bond_to_adj_bonds: Mapping, bonds: list) -> None:
    if set(bond_to_adj_bonds.keys()) != set(bonds):
        raise ValueError('Keys in "bond_adjacency" must be the same as "bonds".')
    
    bonds_set = set(bonds)
    for bond, adj_bonds in bond_to_adj_bonds.items():
        if not all(bond in bonds_set for bond in adj_bonds):
            raise ValueError(
                f'All elements in "bond_adjacency" must be in "bonds". '
                f'Error at bond: {bond}.')


def parse_sym_ops(input_data: Mapping) -> Mapping | None:
    if 'sym_ops_by_bond_maps' in input_data:
        return input_data['sym_ops_by_bond_maps']
    if 'sym_ops_by_bond_perms' in input_data:
        return {
            op_name: cyclic_perms_to_map(op_perm)
            for op_name, op_perm in input_data['sym_ops_by_bond_perms'].items()
        }
    return None


def validate_sym_ops(
        sym_ops: Mapping, bonds: Iterable[_T]
        ) -> None:
    bonds = set(bonds)
    for op_name, op_map in sym_ops.items():
        if set(op_map.keys()) != bonds:
            raise ValueError(
                f'Keys in the operation mapping must contain all bonds. '
                f'Error at operation: {op_name}.')
        if set(op_map.values()) != bonds:
            raise ValueError(
                f'Values in the operation mapping must contain all bonds. '
                f'Error at operation: {op_name}.')


# ============================================================
# Result Formatting and Saving
# ============================================================

def sort_bond_subsets(
        bond_subsets: Iterable[Iterable[_T]]) -> list[list[_T]]:
    """Sort bond subsets for deterministic output.

    This function takes bond subsets and returns them sorted 
    in a consistent order based on the length of each subset 
    and the elements within each subset.

    Parameters
    ----------
    bond_subsets : Iterable[Iterable[_T]]
        The input bond subsets to sort.

    Returns
    -------
    list[list[_T]]
        A sorted list of sorted bond subsets.    
    """
    return sorted(
        [sorted(bondset) for bondset in bond_subsets if bondset],
        key=lambda x: (len(x), x))
