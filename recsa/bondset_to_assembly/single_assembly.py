from collections.abc import Mapping

from recsa import Assembly, Component
from recsa.algorithms.subassembly import bond_induced_sub_assembly

__all__ = ['convert_bondset_to_assembly']


def convert_bondset_to_assembly(
        connected_bond_ids: set[str],
        components: Mapping[str, str],
        bond_id_to_bindsites: dict[str, frozenset[str]],
        comp_kind_to_structure: dict[str, Component]
        ) -> Assembly:
    """Converts the connected bonds to a graph."""
    
    connected_bonds = {
        bond_id_to_bindsites[bond_id] for bond_id in connected_bond_ids}
    
    template = Assembly(
        comp_kind_to_structure,
        components, set(bond_id_to_bindsites.values()))
    
    return bond_induced_sub_assembly(template, connected_bonds)
