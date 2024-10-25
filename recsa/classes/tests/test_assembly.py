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


def test_add_component() -> None:
    assembly = Assembly()
    assembly.add_component('M1', 'M')
    assembly.add_component('L1', 'L')
    assembly.add_components([('X1', 'X'), ('X2', 'X'), ('X3', 'X')])
    assembly.add_bond('M1.a', 'X1.a')
    assembly.add_bonds([
        ('M1.b', 'X1.a'), ('M1.c', 'X2.a'), ('M1.d', 'X3.a')])

    assert assembly.component_id_to_kind == {
        'M1': 'M', 'L1': 'L', 'X1': 'X', 'X2': 'X', 'X3': 'X'}
    assert assembly.bonds == {
        frozenset(['M1.a', 'X1.a']), frozenset(['M1.b', 'X1.a']),
        frozenset(['M1.c', 'X2.a']), frozenset(['M1.d', 'X3.a'])}


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


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
