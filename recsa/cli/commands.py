import click

from recsa.pipelines import (bondsets_to_assemblies_pipeline,
                             enum_bond_subsets_pipeline)


@click.command('enumerate-bond-subsets')
@click.argument('input', type=click.Path(exists=True))
@click.argument('output', type=click.Path())
def run_enum_bond_subset_pipeline(input, output):
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
