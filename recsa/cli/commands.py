import click

from recsa.pipelines import (bondsets_to_assemblies_pipeline,
                             enum_bond_subsets_pipeline,
                             enumerate_assemblies_pipeline)


@click.command('enumerate-assemblies')
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
@click.option(
    '--wip-dir', '-w', type=click.Path(), 
    help='Directory to store intermediate files.')
@click.option(
    '--overwrite', '-o',
    is_flag=True, help='Overwrite output file if it exists.')
@click.option(
    '--verbose', '-v',
    is_flag=True, help='Print verbose output.')
def run_enum_assemblies_pipeline(input, output, wip_dir, overwrite, verbose):
    """Enumerates assemblies.
    
    \b
    Parameters
    ----------
    - INPUT: Path to input file.
    - OUTPUT: Path to output file.

    \b
    Options
    -------
    --wip-dir, -w: Directory to store intermediate files.
    --overwrite, -o: Overwrite output file if it exists.
    --verbose, -v: Print verbose output
    """
    enumerate_assemblies_pipeline(
        input, output,
        wip_dir=wip_dir, overwrite=overwrite, verbose=verbose)


@click.command('enumerate-bond-subsets')
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
def run_enum_bond_subsets_pipeline(input, output):
    """Enumerates bond subsets.
    
    \b
    Parameters
    ----------
    - INPUT: Path to input file.
    - OUTPUT: Path to output file.
    """
    enum_bond_subsets_pipeline(input, output)


@click.command('bondsets-to-assemblies')
@click.argument('bondsets', type=click.Path(exists=True))
@click.argument('structure', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
def run_bondsets_to_assemblies_pipeline(bondsets, structure, output):
    """Converts bondsets to assemblies.
    
    \b
    Parameters
    ----------
    - BONDSETS: Path to input file of bond subsets.
    - STRUCTURE: Path to input file of structure.
    - OUTPUT: Path to output file.
    """
    bondsets_to_assemblies_pipeline(bondsets, structure, output)
