from nasap_net.assembly_enumeration.lib.fragment_enumeration.models import \
    Fragment
from nasap_net.models import Assembly


def fragment_to_assembly(
        fragment: Fragment, template: Assembly
) -> Assembly:
    # NOTE: The conversion from Fragment to Assembly assumes that
    # a pair of component IDs uniquely identifies a bond,
    # which holds true as long as there are no parallel bonds (chelate).
    # This logic needs to be revisited if parallel bonds are to be supported.
    components = {
        comp_id: template.components[comp_id]
        for comp_id in fragment.components
    }
    bonds = [
        template.get_bond_by_comp_ids(*bond.component_ids)
        for bond in fragment.bonds
    ]
    return Assembly(components=components, bonds=bonds)
