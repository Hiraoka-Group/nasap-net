import click

from recsa.pipelines import (bondsets_to_assemblies_pipeline,
                             enum_bond_subsets_pipeline)


@click.command()
@click.option(
    '--input', '-i', type=click.Path(exists=True), required=True, 
    help='Input file path')
@click.option(
    '--output', '-o', type=click.Path(), required=True, 
    help='Output file path')
def run_bond_subset_pipeline(input, output):
    enum_bond_subsets_pipeline(input, output)


@click.command()
@click.option(
    '--bondsets', '-b', type=click.Path(exists=True), required=True,
    help='Path to bond subsets file')
@click.option(
    '--structure', '-s', type=click.Path(exists=True), required=True,
    help='Path to structure data file')
@click.option(
    '--output', '-o', type=click.Path(), required=True,
    help='Output file path')
def run_bondset_to_assembly_pipeline(bondsets, structure, output):
    bondsets_to_assemblies_pipeline(bondsets, structure, output)
