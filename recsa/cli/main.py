import click

from recsa.cli.commands import (run_bondsets_to_assemblies_pipeline,
                                run_enum_bond_subset_pipeline)


@click.group()
def main():
    """RECSA CLI"""
    pass

main.add_command(run_enum_bond_subset_pipeline)
main.add_command(run_bondsets_to_assemblies_pipeline)

if __name__ == '__main__':
    main()
