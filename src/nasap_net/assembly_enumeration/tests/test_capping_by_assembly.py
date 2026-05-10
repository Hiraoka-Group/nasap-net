import pytest

from nasap_net.assembly_enumeration.lib.capping_by_assembly import \
    cap_assemblies_with_assembly
from nasap_net.helpers.assembly_union import ComponentIDCollisionError
from nasap_net.models import Assembly, BindingSite, Bond, Component


@pytest.fixture
def M():
    return Component(kind='M', sites=[0, 1])


@pytest.fixture
def L():
    return Component(kind='L', sites=[0, 1])


@pytest.fixture
def Cap():
    return Component(kind='Cap', sites=[0, 1])


@pytest.fixture
def End():
    return Component(kind='End', sites=[0])


@pytest.fixture
def capping_assembly(Cap, End):
    # (0)Cap(1)---(0)End
    return Assembly(
        components={'C0': Cap, 'E0': End},
        bonds=[Bond('C0', 1, 'E0', 0)],
    )


@pytest.fixture
def capping_site():
    return BindingSite('C0', 0)


def test_single_free_site(M, L, Cap, End, capping_assembly, capping_site):
    fragment = Assembly(
        components={'M0': M, 'L0': L},
        bonds=[Bond('M0', 0, 'L0', 0)],
    )

    result = cap_assemblies_with_assembly(
        assemblies=[fragment],
        capping_assembly=capping_assembly,
        capping_assembly_site=capping_site,
        metal_kinds=['M'],
        return_only_unique=False,
    )

    assert len(result) == 1
    capped = next(iter(result))
    assert capped.components == {
        'M0': M, 'L0': L, 'cap0_C0': Cap, 'cap0_E0': End,
    }
    assert capped.bonds == frozenset({
        Bond('M0', 0, 'L0', 0),
        Bond('cap0_C0', 1, 'cap0_E0', 0),
        Bond('M0', 1, 'cap0_C0', 0),
    })


def test_two_free_sites_get_separate_copies(M, Cap, End, capping_assembly, capping_site):
    fragment = Assembly(
        components={'M0': M},
        bonds=[],
    )

    result = cap_assemblies_with_assembly(
        assemblies=[fragment],
        capping_assembly=capping_assembly,
        capping_assembly_site=capping_site,
        metal_kinds=['M'],
        return_only_unique=False,
    )

    assert len(result) == 1
    capped = next(iter(result))
    assert capped.components == {
        'M0': M,
        'cap0_C0': Cap, 'cap0_E0': End,
        'cap1_C0': Cap, 'cap1_E0': End,
    }
    assert capped.bonds == frozenset({
        Bond('M0', 0, 'cap0_C0', 0),
        Bond('cap0_C0', 1, 'cap0_E0', 0),
        Bond('M0', 1, 'cap1_C0', 0),
        Bond('cap1_C0', 1, 'cap1_E0', 0),
    })


def test_multiple_assemblies_all_capped(M, L, capping_assembly, capping_site):
    fragment1 = Assembly(
        components={'M0': M, 'L0': L},
        bonds=[Bond('M0', 0, 'L0', 0)],
    )
    fragment2 = Assembly(
        components={'M0': M, 'L0': L},
        bonds=[Bond('M0', 0, 'L0', 1)],
    )

    result = cap_assemblies_with_assembly(
        assemblies=[fragment1, fragment2],
        capping_assembly=capping_assembly,
        capping_assembly_site=capping_site,
        metal_kinds=['M'],
        return_only_unique=False,
    )

    assert len(result) == 2


def test_component_id_collision_raises(M, Cap, capping_assembly, capping_site):
    # Fragment already has a component ID matching the cap prefix
    fragment = Assembly(
        components={'M0': M, 'cap0_C0': Cap},
        bonds=[Bond('M0', 0, 'cap0_C0', 0)],
    )
    with pytest.raises(ComponentIDCollisionError):
        cap_assemblies_with_assembly(
            assemblies=[fragment],
            capping_assembly=capping_assembly,
            capping_assembly_site=capping_site,
            metal_kinds=['M'],
            return_only_unique=False,
        )


def test_return_only_unique_deduplicates_isomorphic(M, L, capping_assembly, capping_site):
    # Bond at site 0 vs site 1 of M — isomorphic fragments
    fragment1 = Assembly(
        components={'M0': M, 'L0': L},
        bonds=[Bond('M0', 0, 'L0', 0)],
    )
    fragment2 = Assembly(
        components={'M0': M, 'L0': L},
        bonds=[Bond('M0', 1, 'L0', 0)],
    )

    result_all = cap_assemblies_with_assembly(
        assemblies=[fragment1, fragment2],
        capping_assembly=capping_assembly,
        capping_assembly_site=capping_site,
        metal_kinds=['M'],
        return_only_unique=False,
    )
    result_unique = cap_assemblies_with_assembly(
        assemblies=[fragment1, fragment2],
        capping_assembly=capping_assembly,
        capping_assembly_site=capping_site,
        metal_kinds=['M'],
        return_only_unique=True,
    )

    assert len(result_all) == 2
    assert len(result_unique) == 1
