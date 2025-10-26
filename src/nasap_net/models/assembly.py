from collections.abc import Iterable, Mapping
from dataclasses import dataclass
from functools import cached_property
from types import MappingProxyType
from typing import Any, Self

from frozendict import frozendict

from nasap_net.exceptions import IDNotSetError, NasapNetError
from nasap_net.types import ID
from .binding_site import BindingSite
from .bond import Bond
from .component import Component
from .helper import construct_repr


@dataclass
class InvalidBondError(NasapNetError):
    bond: Bond
    detail: str | None = None

    def __str__(self) -> str:
        base_msg = f'Invalid bond: {self.bond}'
        if self.detail:
            return f'{base_msg} - {self.detail}'
        return base_msg


@dataclass
class InconsistentComponentError(Exception):
    """Raised when there are inconsistent definitions for a component kind,
    i.e., the same kind name corresponds to different component structures.
    """
    component_kind: str
    component1: Component
    component2: Component

    def __str__(self) -> str:
        return (
            f'Inconsistent definitions for component kind '
            f'"{self.component_kind}": '
            f'Component 1: {self.component1}, Component 2: {self.component2}.'
        )


@dataclass(frozen=True, init=False)
class Assembly:
    """An assembly of components connected by bonds.

    Parameters
    ----------
    components : Mapping[C, nasap_net.models.component.Component[S]]
        A mapping from component IDs to their corresponding components.
    bonds : Iterable[Bond[C, S]]
        An iterable of bonds connecting the components.

    Raises
    ------
    - InconsistentComponentError
        If components with the same kind have different structures.
    - InvalidBondError
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
    _id: ID | None

    def __init__(
            self, components: Mapping[ID, Component],
            bonds: Iterable[Bond],
            *,
            id_: ID | None = None
            ):
        object.__setattr__(self, '_components', frozendict(components))
        object.__setattr__(self, 'bonds', frozenset(bonds))
        object.__setattr__(self, '_id', id_)
        self._validate()

    def __repr__(self):
        fields: dict[str, Any] = {}
        if self._id is not None:
            fields['id'] = self._id
        fields['components'] = dict(sorted(self.component_id_to_kind.items()))
        fields['bonds'] = [bond.to_tuple() for bond in sorted(self.bonds)]
        return construct_repr(self.__class__, fields)

    @property
    def id(self) -> ID:
        """Return the ID of the assembly."""
        if self._id is None:
            raise IDNotSetError("Assembly ID is not set.")
        return self._id

    @property
    def id_or_none(self) -> ID | None:
        """Return the ID of the assembly, or None if not set."""
        return self._id

    @property
    def components(self) -> Mapping[ID, Component]:
        """Return the components in the assembly as an immutable mapping."""
        return MappingProxyType(self._components)

    @cached_property
    def component_id_to_kind(self) -> Mapping[ID, str]:
        """Return a mapping from component IDs to their kinds."""
        return MappingProxyType({
            comp_id: comp.kind for comp_id, comp
            in self._components.items()
        })

    def get_component_kind_of_site(self, site: BindingSite) -> str:
        """Return the component kind of the given binding site."""
        return self._components[site.component_id].kind

    def find_sites(
            self, *, has_bond: bool | None = None,
            component_kind: str | None = None
            ) -> frozenset[BindingSite]:
        """Return binding sites based on their bond status.
        """
        if has_bond is None and component_kind is None:
            return self._all_sites

        sites = set()
        for site in self._all_sites:
            if has_bond is not None:
                if has_bond != self.has_bond(site):
                    continue
            if component_kind is not None:
                if self.get_component_kind_of_site(site) != component_kind:
                    continue
            sites.add(site)
        return frozenset(sites)

    def has_bond(self, site: BindingSite) -> bool:
        """Check if a binding site has a bond."""
        return site in self._site_connection

    def add_bond(self, site1: BindingSite, site2: BindingSite):
        """Return a new assembly with an additional bond."""
        new_bond = Bond.from_sites(site1, site2)
        new_bonds = set(self.bonds)
        new_bonds.add(new_bond)
        return self.copy_with(bonds=new_bonds)

    def remove_bond(self, site1: BindingSite, site2: BindingSite):
        """Return a new assembly with a bond removed."""
        bond_to_remove = Bond.from_sites(site1, site2)
        new_bonds = set(self.bonds)
        new_bonds.remove(bond_to_remove)
        return self.copy_with(bonds=new_bonds)

    def copy_with(
            self,
            *,
            components: Mapping[ID, Component] | None = None,
            bonds: Iterable[Bond] | None = None,
            id_: ID | None = None,
            ) -> Self:
        """Return a copy of the assembly with optional modifications."""
        if components is None:
            components = self.components
        if bonds is None:
            bonds = self.bonds
        return self.__class__(
            components=components, bonds=bonds, id_=id_)

    @cached_property
    def _all_sites(self) -> frozenset[BindingSite]:
        """Return all binding sites in the assembly."""
        sites = set()
        for comp_id, component in self._components.items():
            for site in component.site_ids:
                sites.add(BindingSite(component_id=comp_id, site_id=site))
        return frozenset(sites)

    @cached_property
    def _site_connection(self) -> Mapping[BindingSite, BindingSite]:
        """Return a mapping of each binding site to its connected binding site.

        Only bonded sites are included in the mapping.
        """
        connection = {}
        for bond in self.bonds:
            site1, site2 = bond.sites
            connection[site1] = site2
            connection[site2] = site1
        return MappingProxyType(connection)

    def _get_component_of_site(self, site: BindingSite) -> Component:
        """Return the component corresponding to the given binding site."""
        return self._components[site.component_id]

    def _validate(self):
        self._validate_components()
        self._validate_bonds()

    def _validate_components(self):
        # Components with the same kind should have the same structure.
        comp_kind_to_obj: dict[str, Component] = {}
        for comp in self._components.values():
            if comp.kind in comp_kind_to_obj:
                if comp != comp_kind_to_obj[comp.kind]:
                    raise InconsistentComponentError(
                        component_kind=comp.kind,
                        component1=comp,
                        component2=comp_kind_to_obj[comp.kind],
                    )
            else:
                comp_kind_to_obj[comp.kind] = comp

    def _validate_bonds(self):
        component_keys = set(self._components.keys())
        used_sites = set()
        for bond in self.bonds:
            # Validate that the components exist
            for comp_id in bond.component_ids:
                if comp_id not in component_keys:
                    raise InvalidBondError(
                        bond=bond,
                        detail=f"Component {comp_id} not found in assembly.")

            # Validate that the sites exist in the respective components
            for site in bond.sites:
                component = self._components[site.component_id]
                if site.site_id not in component.site_ids:
                    raise InvalidBondError(
                        bond=bond,
                        detail=(
                            f"Site {site.site_id} not found in component "
                            f"{site.component_id}."))

                # Validate that the site is not already used
                if site in used_sites:
                    raise InvalidBondError(
                        bond=bond,
                        detail=f"Site {site} is already used in another bond.")
                used_sites.add(site)
