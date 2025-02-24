import click

from recsa.pipelines import enum_bond_subsets_pipeline


@click.command()
@click.option(
    '--input', '-i', type=click.Path(exists=True), required=True, 
    help='Input file path')
@click.option(
    '--output', '-o', type=click.Path(), required=True, 
    help='Output file path')
def run_bond_subset_pipeline(input, output):
    enum_bond_subsets_pipeline(input, output)
