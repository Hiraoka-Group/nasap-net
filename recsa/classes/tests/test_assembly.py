import pytest

from recsa import Assembly, AuxEdge, Component


@pytest.fixture
def M_COMP() -> Component:
    return Component('M', {'a', 'b', 'c', 'd'})


@pytest.fixture
def M_WITH_AUX_EDGES() -> Component:
    return Component(
        'M', {'a', 'b', 'c', 'd'}, 
        {
            AuxEdge('a', 'b', 'cis'), AuxEdge('b', 'c', 'cis'),
            AuxEdge('c', 'd', 'cis'), AuxEdge('d', 'a', 'cis')
        })


@pytest.fixture
def L_COMP() -> Component:
    return Component('L', {'a', 'b'})


@pytest.fixture
def X_COMP() -> Component:
    return Component('X', {'a'})


def test_init_with_no_args() -> None:
    assembly = Assembly()
    assert assembly.component_id_to_kind == {}
    assert assembly.bonds == set()


def test_init() -> None:
    components = {
        'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X', 'X3': 'X'}
    bonds = {
        frozenset(['M1.a', 'X1.a']), frozenset(['M1.b', 'X1.a']),
        frozenset(['M1.c', 'X2.a']), frozenset(['M1.d', 'X3.a']),}
    assembly = Assembly(components, bonds)

    assert assembly.component_id_to_kind == components
    assert assembly.bonds == set(bonds)


def test_with_added_component() -> None:
    assembly = Assembly()
    new_assembly = assembly.with_added_component('M1', 'M')
    
    assert new_assembly.component_id_to_kind == {'M1': 'M'}
    assert new_assembly.bonds == set()
    assert assembly.component_id_to_kind == {}
    assert assembly.bonds == set()

    new_assembly = new_assembly.with_added_component('L1', 'L')
    
    assert new_assembly.component_id_to_kind == {'M1': 'M', 'L1': 'L'}
    assert new_assembly.bonds == set()
    assert assembly.component_id_to_kind == {}
    assert assembly.bonds == set()


def test_with_added_components() -> None:
    assembly = Assembly()
    new_assembly = assembly.with_added_components([('M1', 'M'), ('L1', 'L')])
    
    assert new_assembly.component_id_to_kind == {'M1': 'M', 'L1': 'L'}
    assert new_assembly.bonds == set()
    assert assembly.component_id_to_kind == {}
    assert assembly.bonds == set()

    new_assembly = new_assembly.with_added_components([('X1', 'X'), ('X2', 'X')])
    
    assert new_assembly.component_id_to_kind == {'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X'}
    assert new_assembly.bonds == set()
    assert assembly.component_id_to_kind == {}
    assert assembly.bonds == set()


def test_with_added_bond() -> None:
    components = {
        'M1': 'M', 'M2': 'M', 'L1': 'L', 'L2': 'L', 
        'X1': 'X', 'X2': 'X'}
    bonds = {
        frozenset(['M1.a', 'L1.a']), frozenset(['M1.b', 'L2.a']),
        frozenset(['M1.c', 'X1.a']), frozenset(['M1.d', 'X2.a']),
        frozenset(['M2.a', 'L1.b'])}
    assembly = Assembly(components, bonds)

    new_assembly = assembly.with_added_bond('M2.b', 'L2.b')
    
    assert new_assembly.component_id_to_kind == components
    assert new_assembly.bonds == bonds | {frozenset(['M2.b', 'L2.b'])}
    assert assembly.component_id_to_kind == components
    assert assembly.bonds == bonds


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
