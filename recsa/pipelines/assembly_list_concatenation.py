import os
from collections.abc import Mapping, Sequence
from typing import Any

from recsa import Assembly
from recsa.pipelines.lib import read_file, write_output


def concatenate_assemblies_pipeline(
        assemblies_path_list: Sequence[os.PathLike | str],
        resulting_assems_path: os.PathLike | str,
        *,
        start: int = 0,
        overwrite: bool = False,
        verbose: bool = False,
        ) -> None:
    """Concatenate a list of assemblies into a single list.
    
    Concatenates a list of assemblies from different files into a single 
    list. The IDs of the assemblies are reindexed starting from the given
    start value.

    Parameters
    ----------
    assemblies_path_list : Sequence[os.PathLike | str]
        List of paths to the files containing the assemblies.
        Each file should contain a dictionary with the assembly IDs as keys
        and the Assembly objects as values.
    resulting_assems_path : os.PathLike | str
        Path to the file to save the concatenated list of assemblies.
    start : int, optional
        Starting index for the reindexing of the assemblies, by default 0.
    overwrite : bool, optional
        Whether to overwrite the file if it already exists, by default False.
    verbose : bool, optional
        Whether to print the process steps, by default False
    
    Notes
    -----
    The reindexing order is determined by the order of the input files and 
    the order of the assemblies in each file, not by their alphabetical 
    order.

    Output file contains a dictionary with the reindexed IDs as keys and the
    Assembly objects as values.
    """
    # Input
    list_of_id_to_assembly: Sequence[Mapping[Any, Assembly]] = [
        read_file(path, verbose=verbose)
        for path in assemblies_path_list]
    
    # Main process
    if verbose:
        print('Concatenating assembly lists...')

    assemblies: list[Assembly] = []
    for id_to_assembly in list_of_id_to_assembly:
        assemblies.extend(id_to_assembly.values())
    
    reindexed = {
        new_id: assems for new_id, assems 
        in enumerate(assemblies, start=start)
    }
    
    if verbose:
        print('Concatenation completed.')

    # Save reindexed assemblies
    write_output(
        resulting_assems_path, reindexed,
        overwrite=overwrite, verbose=verbose,
        header='Concatenated list of assemblies')
