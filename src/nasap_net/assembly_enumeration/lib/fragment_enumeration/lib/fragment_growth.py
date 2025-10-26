from collections.abc import Iterable, Iterator

from nasap_net.types import ID
from ..models import Fragment, LightBond


def grow_fragment(
        fragment: Fragment, template: Fragment
) -> Iterator[Fragment]:
    for bond in sorted(_enumerate_new_bonds(fragment, template)):
        yield _add_bond_to_fragment(fragment, bond)


def _enumerate_new_bonds(
        fragment: Fragment, template: Fragment
) -> frozenset[LightBond]:
    """Enumerate possible bonds that can be added to the fragment
    with or without adding new components.
    """
    existing_bonds = fragment.bonds
    candidate_bonds = _get_bonds_of_components(template, fragment.components)
    return candidate_bonds - existing_bonds


def _get_bonds_of_components(
        fragment: Fragment, components: Iterable[ID]
) -> frozenset[LightBond]:
    """Get all bonds in the fragment that involve the specified components."""
    bonds = set()
    for bond in fragment.bonds:
        if not bond.component_ids.isdisjoint(components):
            bonds.add(bond)
    return frozenset(bonds)


def _add_bond_to_fragment(fragment: Fragment, bond: LightBond) -> Fragment:
    """Create a new fragment by adding the specified bond"""
    if missing_comps := bond.component_ids - fragment.components:
        # Bond involves a new component
        assert len(missing_comps) == 1
        new_comp_id = next(iter(missing_comps))
        new_components = frozenset({*fragment.components, new_comp_id})
    else:
        new_components = fragment.components
    new_bonds = [*fragment.bonds, bond]
    return fragment.copy_with(components=new_components, bonds=new_bonds)
