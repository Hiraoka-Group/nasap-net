from collections.abc import Iterable, Iterator
from dataclasses import dataclass

from nasap_net.types import ID, SupportsDunderLt
from .binding_site import BindingSite


@dataclass(frozen=True, init=False, order=True)
class Bond(Iterable, SupportsDunderLt):
    """A bond between two binding sites on two components."""
    sites: tuple[BindingSite, BindingSite]

    def __init__(self, comp_id1: ID, site1: ID, comp_id2: ID, site2: ID):
        if comp_id1 == comp_id2:
            raise ValueError("Components in a bond must be different.")
        comp_and_site1 = BindingSite(component_id=comp_id1, site_id=site1)
        comp_and_site2 = BindingSite(component_id=comp_id2, site_id=site2)
        object.__setattr__(
            self, 'sites',
            tuple(sorted((comp_and_site1, comp_and_site2))))  # type:ignore

    def __iter__(self) -> Iterator[BindingSite]:
        return iter(self.sites)

    @property
    def component_ids(self) -> tuple[ID, ID]:
        """Return the component IDs involved in the bond."""
        return self.sites[0].component_id, self.sites[1].component_id

    @classmethod
    def from_sites(cls, site1: BindingSite, site2: BindingSite) -> 'Bond':
        """Create a Bond from two BindingSite instances."""
        return cls(
            comp_id1=site1.component_id,
            comp_id2=site2.component_id,
            site1=site1.site_id,
            site2=site2.site_id
            )
