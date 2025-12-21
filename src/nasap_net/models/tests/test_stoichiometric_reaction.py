import pytest
from frozendict import frozendict

from nasap_net import StoichiometricReaction


def test_creation_and_str_repr():
    r = StoichiometricReaction({'A': 2, 'B': 1}, {'C': 3}, 1)
    assert isinstance(r.reactants, frozendict)
    assert isinstance(r.products, frozendict)
    assert r.equation_str == '2A + B -> 3C'
    assert str(r) == '2A + B -> 3C (x1)'
    assert repr(r) == '<StoichiometricReaction 2A + B -> 3C>'


def test_repr_with_id():
    r = StoichiometricReaction({'A': 1}, {'B': 1}, 1, id_='R1')
    assert repr(r) == '<StoichiometricReaction ID=R1: A -> B>'


def test_equation_str_coefficients():
    r = StoichiometricReaction({'A': 1, 'B': 2}, {'C': 1}, 1)
    assert r.equation_str == 'A + 2B -> C'


def test_empty_reactants_products():
    r = StoichiometricReaction({}, {}, 1)
    assert r.equation_str == ' -> '


@pytest.mark.parametrize('dup', [0, -1])
def test_invalid_duplicate_count(dup):
    with pytest.raises(ValueError):
        StoichiometricReaction({'A': 1}, {'B': 1}, dup)


def test_immutability():
    r = StoichiometricReaction({'A': 1}, {'B': 1}, 1)
    with pytest.raises(TypeError):
        r.reactants['A'] = 5  # type: ignore
    with pytest.raises(TypeError):
        r.products['B'] = 5  # type: ignore


def test_mapping_types():
    r1 = StoichiometricReaction({'A': 1}, {'B': 1}, 1)
    r2 = StoichiometricReaction(frozendict({'A': 1}), frozendict({'B': 1}), 1)
    assert r1.reactants == r2.reactants
    assert r1.products == r2.products
