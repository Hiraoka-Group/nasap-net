import pytest

from nasap_net import Assembly, BindingSite, Reaction, StoichiometricReaction


def test_creation_and_str_repr():
    r = StoichiometricReaction('A', 'B', 'C', None, 1)
    assert r.reactant1 == 'A'
    assert r.reactant2 == 'B'
    assert r.product1 == 'C'
    assert r.product2 is None
    assert r.equation_str == 'A + B -> C'
    assert str(r) == 'A + B -> C (x1)'
    assert repr(r) == '<StoichiometricReaction (A + B -> C)>'


def test_repr_with_id():
    r = StoichiometricReaction('A', None, 'B', None, 1, id_='R1')
    assert repr(r) == '<StoichiometricReaction ID=R1 (A -> B)>'


def test_equation_str_variants():
    r1 = StoichiometricReaction('A', None, 'C', None, 1)
    assert r1.equation_str == 'A -> C'
    r2 = StoichiometricReaction('A', 'B', 'C', 'D', 2)
    assert r2.equation_str == 'A + B -> C + D'
    r3 = StoichiometricReaction('A', None, 'C', 'D', 3)
    assert r3.equation_str == 'A -> C + D'
    r4 = StoichiometricReaction('A', 'B', 'C', None, 4)
    assert r4.equation_str == 'A + B -> C'


def test_invalid_duplicate_count():
    with pytest.raises(ValueError):
        StoichiometricReaction('A', None, 'B', None, 0)
    with pytest.raises(ValueError):
        StoichiometricReaction('A', None, 'B', None, -1)


def test_none_reactant1_or_product1():
    with pytest.raises(ValueError):
        StoichiometricReaction(None, 'B', 'C', None, 1)  # type: ignore
    with pytest.raises(ValueError):
        StoichiometricReaction('A', None, None, 'D', 1)  # type: ignore


def test_from_reaction():
    reaction = Reaction(
        init_assem=Assembly(id_='A', components={}, bonds=[]),
        entering_assem=Assembly(id_='B', components={}, bonds=[]),
        product_assem=Assembly(id_='C', components={}, bonds=[]),
        leaving_assem=None,
        metal_bs=BindingSite('metal', 0),
        leaving_bs=BindingSite('leaving', 0),
        entering_bs=BindingSite('entering', 0),
        duplicate_count=2,
        id_='R1',
    )

    stoich_reaction = StoichiometricReaction.from_reaction(reaction)

    assert stoich_reaction.reactant1 == 'A'
    assert stoich_reaction.reactant2 == 'B'
    assert stoich_reaction.product1 == 'C'
    assert stoich_reaction.product2 is None
    assert stoich_reaction.duplicate_count == 2
    assert stoich_reaction.id_ == 'R1'


def test_reactants_products_changes():
    # A + B -> C
    r1 = StoichiometricReaction('A', 'B', 'C', None, 1)
    assert r1.reactants == {'A': 1, 'B': 1}
    assert r1.products == {'C': 1}
    assert r1.changes == {'A': -1, 'B': -1, 'C': 1}

    # A -> B + C
    r2 = StoichiometricReaction('A', None, 'B', 'C', 1)
    assert r2.reactants == {'A': 1}
    assert r2.products == {'B': 1, 'C': 1}
    assert r2.changes == {'A': -1, 'B': 1, 'C': 1}

    # A -> B
    r3 = StoichiometricReaction('A', None, 'B', None, 1)
    assert r3.reactants == {'A': 1}
    assert r3.products == {'B': 1}
    assert r3.changes == {'A': -1, 'B': 1}

    # A + A -> B
    r4 = StoichiometricReaction('A', 'A', 'B', None, 1)
    assert r4.reactants == {'A': 2}
    assert r4.products == {'B': 1}
    assert r4.changes == {'A': -2, 'B': 1}

    # A -> A
    r5 = StoichiometricReaction('A', None, 'A', None, 1)
    assert r5.reactants == {'A': 1}
    assert r5.products == {'A': 1}
    assert r5.changes == {'A': 0}
