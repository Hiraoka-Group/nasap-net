from collections.abc import Iterable, Mapping
from typing import TypeVar

from nasap_net.models import Assembly, Component
from nasap_net.types import ID
from .lib import cap_fragments_with_ligand, enumerate_fragments, \
    extract_unique_assemblies_by_isomorphism

_T = TypeVar('_T', bound=ID)


def enumerate_assemblies(
        template: Assembly,
        *,
        leaving_ligand: Component,
        symmetry_operations: Iterable[Mapping[_T, ID]] | None = None
) -> list[Assembly]:
    """Enumerate assemblies which can be formed by adding the leaving ligand
    to the fragments of the template assembly.

    This function generates all possible assemblies by attaching the
    specified leaving ligand to each fragment in the template assembly. It
    ensures that the resulting assemblies are unique by excluding duplicates
    based on symmetry operations and isomorphism checks.

    Any two assemblies that meet either of the following conditions are
    considered duplicates, and only one of them is included in the output list:
    - One can be transformed into the other by applying a symmetry operation
      from the provided list.
    - They are isomorphic, i.e., they have the same connectivity structure.

    Providing symmetry operations is strongly recommended to reduce the
    computational cost of duplicate exclusion.

    Parameters
    ----------
    template : Assembly
        The template assembly to base the enumeration on.
    leaving_ligand : Component
        The leaving ligand component to be added to the fragments.
    symmetry_operations : Iterable[Mapping[_T, ID]] | None, optional
        A list of symmetry operations represented as mappings from original
        component IDs to transformed component IDs. If None, no symmetry
        operations are considered.

    Returns
    -------
    list[Assembly]
        A list of unique assemblies formed by adding the leaving ligand
        to the fragments of the template assembly.
    """
    fragments = enumerate_fragments(
        template,
        symmetry_operations=symmetry_operations
    )
    unique_fragments = extract_unique_assemblies_by_isomorphism(
        fragments,
    )
    capped_assemblies = cap_fragments_with_ligand(
        unique_fragments,
        leaving_ligand=leaving_ligand
    )
    return capped_assemblies
