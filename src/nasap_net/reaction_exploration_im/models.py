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

    @classmethod
    def from_sites(cls, site1: BindingSite, site2: BindingSite) -> 'Bond':
        """Create a Bond from two BindingSite instances."""
        return cls(
            comp_id1=site1.component_id,
            comp_id2=site2.component_id,
            site1=site1.site,
            site2=site2.site
            )



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
                    raise InvalidBondError(
                        bond=bond,
                        msg=f"Component {comp_id} not found in assembly.")

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
                    raise InvalidBondError(
                        bond=bond,
                        msg=f"Site {site} is already used in another bond.")
                used_sites.add(site)

    @property
    def components(self) -> Mapping[ID, Component]:
        """Return the components in the assembly as an immutable mapping."""
        return MappingProxyType(self._components)

    def _get_component_of_site(self, site: BindingSite) -> Component:
        """Return the component corresponding to the given binding site."""
        return self._components[site.component_id]

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

    @cached_property
    def _all_sites(self) -> frozenset[BindingSite]:
        """Return all binding sites in the assembly."""
        sites = set()
        for comp_id, component in self._components.items():
            for site in component.site_ids:
                sites.add(BindingSite(component_id=comp_id, site=site))
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
            components: Mapping[ID, Component] | None = None,
            bonds: Iterable[Bond] | None = None
            ) -> 'Assembly':
        """Return a copy of the assembly with optional modifications."""
        if components is None:
            components = self.components
        if bonds is None:
            bonds = self.bonds
        return Assembly(components=components, bonds=bonds)


class AssemblyWithID(Assembly):
    _id: ID

    """An assembly with an associated ID."""
    def __init__(
            self,
            id_: ID,
            components: Mapping[ID, Component],
            bonds: Iterable[Bond]
            ):
        super().__init__(components=components, bonds=bonds)
        object.__setattr__(self, '_id', id_)

    @property
    def id(self) -> ID:
        """Return the ID of the assembly."""
        return self._id

    @classmethod
    def from_assembly(
            cls, id_: ID, assembly: Assembly
            ) -> 'AssemblyWithID':
        """Create an AssemblyWithID from an existing Assembly and an ID."""
        return cls(
            id_=id_,
            components=assembly.components,
            bonds=assembly.bonds
            )

    def copy_with(
            self,
            id_: ID | None = None,
            components: Mapping[ID, Component] | None = None,
            bonds: Iterable[Bond] | None = None
            ) -> 'AssemblyWithID':
        """Return a copy of the assembly with optional modifications."""
        if id_ is None:
            id_ = self.id
        if components is None:
            components = self.components
        if bonds is None:
            bonds = self.bonds
        return AssemblyWithID(id_=id_, components=components, bonds=bonds)


@dataclass(frozen=True)
class MLEKind:
    metal: str
    leaving: str
    entering: str


@dataclass(frozen=True)
class MLE:
    metal: BindingSite
    leaving: BindingSite
    entering: BindingSite


@dataclass(frozen=True)
class MLEWithDup:
    metal: BindingSite
    leaving: BindingSite
    entering: BindingSite
    duplication: int


@dataclass(frozen=True)
class ReactionCandidate:
    init_assem: AssemblyWithID
    entering_assem: AssemblyWithID | None
    product_assem: Assembly
    leaving_assem: Assembly | None
    metal_bs: BindingSite
    leaving_bs: BindingSite
    entering_bs: BindingSite
    duplicate_count: int

    @property
    def init_assem_id(self) -> ID:
        return self.init_assem.id

    @property
    def entering_assem_id(self) -> ID | None:
        if self.entering_assem is None:
            return None
        return self.entering_assem.id


@dataclass(frozen=True)
class Reaction:
    init_assem_id: AssemblyWithID
    entering_assem_id: AssemblyWithID | None
    product_assem_id: AssemblyWithID
    leaving_assem_id: AssemblyWithID | None
    metal_bs: BindingSite
    leaving_bs: BindingSite
    entering_bs: BindingSite
    duplicate_count: int

MLX = Assembly(
    components={
        'M1': Component(kind='M', sites={1, 2}),
        'L1': Component(kind='L', sites={1, 2}),
        'X1': Component(kind='X', sites={1}),
    },
    bonds=[
        Bond('M1', 'L1', 1, 1),
        Bond('M1', 'X1', 2, 1),
    ]
)
