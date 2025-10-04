from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from types import MappingProxyType
from typing import Generic

from frozendict import frozendict

from nasap_net.types import C, S


@dataclass(frozen=True, init=False)
class Component(Generic[S]):
    """Component"""
    kind: str
    sites: frozenset[S]

    def __init__(self, kind: str, sites: Iterable[S]):
        object.__setattr__(self, 'kind', kind)
        object.__setattr__(self, 'sites', frozenset(sites))


@dataclass(frozen=True, order=True)
class BindingSite(Generic[C, S]):
    """A specific binding site on a specific component."""
    component_id: C
    site: S


@dataclass(frozen=True, init=False)
class Bond(Generic[C, S]):
    """A bond between two binding sites on two components."""
    sites: tuple[BindingSite[C, S], BindingSite[C, S]]

    def __init__(self, comp_id1: C, comp_id2: C, site1: S, site2: S):
        if comp_id1 == comp_id2:
            raise ValueError("Components in a bond must be different.")
        comp_and_site1 = BindingSite(component_id=comp_id1, site=site1)
        comp_and_site2 = BindingSite(component_id=comp_id2, site=site2)
        object.__setattr__(
            self, 'sites',
            tuple(sorted((comp_and_site1, comp_and_site2))))  # type:ignore

    @property
    def component_ids(self) -> tuple[C, C]:
        """Return the component IDs involved in the bond."""
        return self.sites[0].component_id, self.sites[1].component_id


@dataclass(frozen=True, init=False)
class Assembly(Generic[C, S]):
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
    _components: frozendict[C, Component[S]]
    bonds: frozenset[Bond[C, S]]

    def __init__(
            self,
            components: Mapping[C, Component[S]],
            bonds: Iterable[Bond[C, S]]
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
                if site.site not in component.sites:
                    raise ValueError(
                        f"Site {site.site} in bond {bond} not found "
                        f"in component {site.component_id} sites.")

                # Validate that the site is not already used
                if site in used_sites:
                    raise ValueError(
                        f"Site {site} in bond {bond} is already used in "
                        f"another bond.")
                used_sites.add(site)

    @property
    def components(self) -> Mapping[C, Component[S]]:
        """Return the components in the assembly as an immutable mapping."""
        return MappingProxyType(self._components)
