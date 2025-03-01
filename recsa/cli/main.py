import click

from recsa.cli.commands import run_bond_subset_pipeline


@click.group()
def main():
    """RECSA CLI"""
    pass

main.add_command(run_bond_subset_pipeline, name='enum-bond-subsets')

if __name__ == '__main__':
    main()
