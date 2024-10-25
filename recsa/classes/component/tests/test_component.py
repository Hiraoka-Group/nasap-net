import pytest

from recsa import AuxEdge, Component, RecsaValueError


@pytest.fixture
def comp() -> Component:
    return Component({'a', 'b'})


@pytest.fixture
def comp_with_aux_edges() -> Component:
    return Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})


def test_init_with_valid_args(comp) -> None:
    assert set(comp.bindsites) == {'a', 'b'}


def test_init_with_valid_args_with_single_aux_edge(comp_with_aux_edges) -> None:
    assert set(comp_with_aux_edges.bindsites) == {'a', 'b'}
    assert comp_with_aux_edges.aux_edges == {AuxEdge('a', 'b', 'cis')}


def test_init_with_valid_args_with_multiple_aux_edges() -> None:
    component = Component({'a', 'b', 'c'}, {
        AuxEdge('a', 'b', 'cis'), AuxEdge('a', 'c', 'cis'), 
        AuxEdge('b', 'c', 'trans')})
    
    assert set(component.bindsites) == {'a', 'b', 'c'}
    assert component.aux_edges == {
        AuxEdge('a', 'b', 'cis'), AuxEdge('a', 'c', 'cis'), 
        AuxEdge('b', 'c', 'trans')}


def test_init_with_invalid_aux_edge_whose_binding_sites_not_in_binding_sites() -> None:
    with pytest.raises(RecsaValueError):
        Component({'a', 'b'}, {AuxEdge('a', 'c', 'cis')})


def test_init_with_empty_binding_sites() -> None:
    # Empty binding sites is allowed.
    component = Component(set())
    assert component.bindsites == frozenset()


def test_init_with_empty_aux_edges() -> None:
    # Empty aux_edges is allowed.
    component = Component({'a', 'b'}, set())
    assert component.aux_edges == frozenset()


def test_init_with_aux_edge_as_tuple() -> None:
    component = Component({'a', 'b'}, [('a', 'b', 'cis')])
    assert component.aux_edges == {AuxEdge('a', 'b', 'cis')}


def test_eq() -> None:
    component1 = Component({'a', 'b'})
    component2 = Component({'a', 'b'})
    component3 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    component4 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'trans')})

    assert component1 == component2
    assert component1 != component3
    assert component3 != component4


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
