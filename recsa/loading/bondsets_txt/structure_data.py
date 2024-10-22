from typing import TypedDict

import yaml

__all__ = ['load_structure_data', 'format_component_instances', 'format_bonds']


class ComponentInstanceDict(TypedDict):
    id: str
    template: str


class BondDict(TypedDict):
    id: str
    bindsites: list[str]


class YamlDict(TypedDict):
    component_instances: list[ComponentInstanceDict]
    bonds: list[BondDict]


def load_structure_data(
        filepath: str
        ) -> tuple[dict[str, str], dict[str, frozenset[str]]]:
    """Parse the input file for `translate_to_graph`."""
    # parse yaml file
    with open(filepath) as f:
        data: YamlDict = yaml.safe_load(f)

    # Format the data
    component_instances = format_component_instances(
        data['component_instances'])
    bond_id_to_bindsites = format_bonds(data['bonds'])

    component_id_to_kind = {}
    for component_id, component_kind in component_instances.items():
        component_id_to_kind[component_id] = component_kind

    # TODO: Add validation

    return component_id_to_kind, bond_id_to_bindsites


def format_component_instances(
        component_instances: list[ComponentInstanceDict]
        ) -> dict[str, str]:
    """Format the components."""
    return {
        x['id']: x['template'] for x in component_instances}


def format_bonds(bonds: list[BondDict]) -> dict[str, frozenset[str]]:
    """Format the bonds."""
    return {
        str(bond['id']): frozenset(bond['bindsites']) for bond in bonds}
