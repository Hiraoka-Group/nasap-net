from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from functools import cached_property
from types import MappingProxyType

from frozendict import frozendict

from nasap_net.types import ID


@dataclass(frozen=True, order=True)
class BindingSite:
    """A specific binding site on a specific component."""
    component_id: ID
    site: ID


@dataclass(frozen=True, order=True)
class BindingSiteWithDup:
    """A specific binding site on a specific component with duplication count."""
    component_id: ID
    site: ID
    duplication: int


@dataclass(frozen=True, init=False)
class Bond:
    """A bond between two binding sites on two components."""
    sites: tuple[BindingSite, BindingSite]

    def __init__(self, comp_id1: ID, comp_id2: ID, site1: ID, site2: ID):
        if comp_id1 == comp_id2:
            raise ValueError("Components in a bond must be different.")
        comp_and_site1 = BindingSite(component_id=comp_id1, site=site1)
        comp_and_site2 = BindingSite(component_id=comp_id2, site=site2)
        object.__setattr__(
            self, 'sites',
            tuple(sorted((comp_and_site1, comp_and_site2))))  # type:ignore

    @property
    def component_ids(self) -> tuple[ID, ID]:
        """Return the component IDs involved in the bond."""
        return self.sites[0].component_id, self.sites[1].component_id


@dataclass(frozen=True)
class AuxEdge:
    """An auxiliary edge between two binding sites on the same component."""
    site1: ID
    site2: ID
    kind: str | None = None


@dataclass(frozen=True, init=False)
class Component:
    """Component"""
    kind: str
    site_ids: frozenset[ID]
    aux_edges: frozenset[AuxEdge]

    def __init__(
            self, kind: str, sites: Iterable[ID],
            aux_edges: Iterable[AuxEdge] | None = None
            ):
        object.__setattr__(self, 'kind', kind)
        object.__setattr__(self, 'sites', frozenset(sites))
        if aux_edges is None:
            aux_edges = frozenset()
        else:
            aux_edges = frozenset(aux_edges)
        object.__setattr__(self, 'aux_edges', aux_edges)


class InvalidBondError(Exception):
    def __init__(self, *, bond: Bond, msg: str = ""):
        self.bond = bond
        combined_msg = f"Invalid bond: {bond}"
        if msg:
            combined_msg += f" - {msg}"
        super().__init__(combined_msg)


@dataclass(frozen=True, init=False)
class Assembly:
    """An assembly of components connected by bonds.

    Parameters
    ----------
    components : Mapping[C, Component[S]]
        A mapping from component IDs to their corresponding components.
    bonds : Iterable[Bond[C, S]]
        An iterable of bonds connecting the components.

    Raises
    ------
    ValueError
        - If any bond references a non-existent component or site.
        - If a component bonds to itself.
        - If a site is used more than once.
        - If the assembly is not connected.

    Warnings
    --------
    - The assembly does not enforce connectivity; it is the user's
      responsibility to ensure that the assembly is connected as needed.
    """
    _components: frozendict[ID, Component]
    bonds: frozenset[Bond]

    def __init__(
            self, components: Mapping[ID, Component],
            bonds: Iterable[Bond],
            ):
        object.__setattr__(self, '_components', frozendict(components))
        object.__setattr__(self, 'bonds', frozenset(bonds))
        self._validate()

    def _validate(self):
        component_keys = set(self._components.keys())
        used_sites = set()
        for bond in self.bonds:
            # Validate that the components exist
            for comp_id in bond.component_ids:
                if comp_id not in component_keys:
                    raise ValueError(
                        f"Component {comp_id} in bond {bond} not found in "
                        f"assembly components.")

            # Validate that the sites exist in the respective components
            for site in bond.sites:
                component = self._components[site.component_id]
                if site.site not in component.site_ids:
                    raise InvalidBondError(
                        bond=bond,
                        msg=(
                            f"Site {site.site} not found in component "
                            f"{site.component_id}."))

                # Validate that the site is not already used
                if site in used_sites:
                    raise ValueError(
                        f"Site {site} in bond {bond} is already used in "
                        f"another bond.")
                used_sites.add(site)

    @property
    def components(self) -> Mapping[ID, Component]:
        """Return the components in the assembly as an immutable mapping."""
        return MappingProxyType(self._components)
