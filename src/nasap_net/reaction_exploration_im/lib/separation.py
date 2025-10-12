from collections.abc import Iterable

from nasap_net.reaction_exploration_im.lib.igraph import \
    convert_assembly_to_igraph
from nasap_net.reaction_exploration_im.models import Assembly
from nasap_net.types import ID


class SeparatedIntoMoreThanTwoPartsError(Exception):
    pass


def separate_if_possible(
        assembly: Assembly,
        metal_comp_id: ID
        ) -> tuple[Assembly, Assembly | None]:
    """Separate the assembly into product and leaving assemblies if possible.

    Assembly ID will be set to None for both assemblies.
    """
    conv_res = convert_assembly_to_igraph(assembly)
    g = conv_res.graph

    group_of_each_vertex: list[int] = g.components().membership
    g1_comp = set()
    g2_comp = set()
    for v_index, group in enumerate(group_of_each_vertex):
        if v_index not in conv_res.core_mapping.inv:
            continue
        comp_id = conv_res.core_mapping.inv[v_index]
        match group:
            case 0:
                g1_comp.add(comp_id)
            case 1:
                g2_comp.add(comp_id)
            case _:
                raise SeparatedIntoMoreThanTwoPartsError()
    if not g2_comp:
        return assembly, None
    assem1 = create_sub_assembly(assembly, g1_comp)
    assem2 = create_sub_assembly(assembly, g2_comp)

    if metal_comp_id in assem1.components:
        return assem1, assem2
    else:
        assert metal_comp_id in assem2.components
        return assem2, assem1


def create_sub_assembly(assembly: Assembly, comp_ids: Iterable[ID]) -> Assembly:
    """Create a sub-assembly containing only the specified components.

    Assembly ID will be set to None.
    """
    new_components = {
        comp_id: comp
        for comp_id, comp in assembly.components.items()
        if comp_id in comp_ids
    }
    new_bonds = [
        bond for bond in assembly.bonds
        if set(bond.component_ids) <= set(comp_ids)
    ]
    return assembly.copy_with(components=new_components, bonds=new_bonds)
