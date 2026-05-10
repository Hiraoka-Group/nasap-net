import pytest

from nasap_net.assembly_enumeration.lib.substitution_with_assembly import \
    enumerate_substitutions_with_assembly
from nasap_net.models import Assembly, BindingSite, Bond, Component


@pytest.fixture
def M():
    return Component(kind='M', sites=[0, 1])


@pytest.fixture
def X():
    return Component(kind='X', sites=[0])


@pytest.fixture
def Cap():
    return Component(kind='Cap', sites=[0, 1])


@pytest.fixture
def End():
    return Component(kind='End', sites=[0])


@pytest.fixture
def substituting_assembly(Cap, End):
    # (0)Cap(1)---(0)End
    return Assembly(
        components={'C0': Cap, 'E0': End},
        bonds=[Bond('C0', 1, 'E0', 0)],
    )


@pytest.fixture
def substituting_site():
    return BindingSite('C0', 0)


@pytest.fixture
def m_capped_with_x(M, X):
    # M0 with both sites capped by X: X0---(0)M0(1)---X1
    return Assembly(
        components={'M0': M, 'X0': X, 'X1': X},
        bonds=[Bond('M0', 0, 'X0', 0), Bond('M0', 1, 'X1', 0)],
    )


def test_single_ligand_yields_one_substitution(M, X, substituting_assembly, substituting_site, Cap, End):
    # (1)M0(0)---(0)X0
    assembly = Assembly(
        components={'M0': M, 'X0': X},
        bonds=[Bond('M0', 0, 'X0', 0)],
    )

    result = enumerate_substitutions_with_assembly(
        assemblies=[assembly],
        leaving_ligand_kind='X',
        substituting_assembly=substituting_assembly,
        substituting_assembly_site=substituting_site,
    )

    assert len(result) == 1
    substituted = next(iter(result))

    # (1)M0(0)---(0)Cap(1)---(0)End
    assert substituted.components == {
        'M0': M, 'sub0_C0': Cap, 'sub0_E0': End,
    }
    assert substituted.bonds == frozenset({
        Bond('M0', 0, 'sub0_C0', 0),
        Bond('sub0_C0', 1, 'sub0_E0', 0),
    })


def test_two_ligands_yield_three_raw_substitutions(m_capped_with_x, substituting_assembly, substituting_site):
    # {X0}, {X1}, {X0, X1} — 3 combinations before deduplication
    from nasap_net.assembly_enumeration.lib.substitution_with_assembly import \
        _enumerate_substitutions

    result = _enumerate_substitutions(
        assembly=m_capped_with_x,
        leaving_ligand_kind='X',
        substituting_assembly=substituting_assembly,
        substituting_assembly_site=substituting_site,
    )

    assert len(result) == 3


def test_deduplication_merges_isomorphic_single_substitutions(m_capped_with_x, substituting_assembly, substituting_site):
    # Replacing X0 vs X1 are isomorphic (M's sites are symmetric)
    # X0(0)---(0)M0(1)---X1(0)
    result = enumerate_substitutions_with_assembly(
        assemblies=[m_capped_with_x],
        leaving_ligand_kind='X',
        substituting_assembly=substituting_assembly,
        substituting_assembly_site=substituting_site,
    )

    # {X0}≅{X1} → 2 unique: one single-substitution, one double-substitution
    assert len(result) == 2


def test_multiple_input_assemblies(M, X, substituting_assembly, substituting_site):
    assembly1 = Assembly(
        components={'M0': M, 'X0': X},
        bonds=[Bond('M0', 0, 'X0', 0)],
    )
    assembly2 = Assembly(
        components={'M0': M, 'X0': X},
        bonds=[Bond('M0', 1, 'X0', 0)],
    )

    result = enumerate_substitutions_with_assembly(
        assemblies=[assembly1, assembly2],
        leaving_ligand_kind='X',
        substituting_assembly=substituting_assembly,
        substituting_assembly_site=substituting_site,
    )

    # assembly1 and assembly2 are isomorphic → 1 unique substitution
    assert len(result) == 1
