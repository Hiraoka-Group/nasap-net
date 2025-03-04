import click

from recsa.cli.commands import (run_bond_subset_pipeline,
                                run_bondset_to_assembly_pipeline)


@click.group()
def main():
    """RECSA CLI"""
    pass

main.add_command(run_bond_subset_pipeline, name='enum-bond-subsets')
main.add_command(run_bondset_to_assembly_pipeline, name='bondset-to-assembly')

if __name__ == '__main__':
    main()
