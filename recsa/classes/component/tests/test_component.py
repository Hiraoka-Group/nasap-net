import pytest

from recsa import AuxEdge, Component, RecsaValueError


@pytest.fixture
def comp() -> Component:
    return Component('M', {'a', 'b'})

@pytest.fixture
def comp_with_aux_edges() -> Component:
    return Component('M', {'a', 'b'}, {AuxEdge('a', 'b', 'cis')})


def test_init_with_valid_args(comp) -> None:
    assert comp.kind == 'M'
    assert set(comp.bindsites) == {'a', 'b'}


def test_init_with_valid_args_with_single_aux_edge(comp_with_aux_edges) -> None:
    assert comp_with_aux_edges.kind == 'M'
    assert set(comp_with_aux_edges.bindsites) == {'a', 'b'}
    assert comp_with_aux_edges.aux_edges == {AuxEdge('a', 'b', 'cis')}


def test_init_with_valid_args_with_multiple_aux_edges() -> None:
    component = Component('M', {'a', 'b', 'c'}, {
        AuxEdge('a', 'b', 'cis'), AuxEdge('a', 'c', 'cis'), 
        AuxEdge('b', 'c', 'trans')})
    
    assert component.kind == 'M'
    assert set(component.bindsites) == {'a', 'b', 'c'}
    assert component.aux_edges == {
        AuxEdge('a', 'b', 'cis'), AuxEdge('a', 'c', 'cis'), 
        AuxEdge('b', 'c', 'trans')}


def test_init_with_invalid_aux_edge_whose_binding_sites_not_in_binding_sites() -> None:
    with pytest.raises(RecsaValueError):
        Component('M', {'a', 'b'}, {AuxEdge('a', 'c', 'cis')})


def test_init_with_empty_binding_sites() -> None:
    # Empty binding sites is allowed.
    component = Component('M', set())
    assert component.bindsites == set()


def test_init_with_empty_aux_edges() -> None:
    # Empty aux_edges is allowed.
    component = Component('M', {'a', 'b'}, set())
    assert component.aux_edges == set()


def test_eq() -> None:
    component1 = Component('M', {'a', 'b'})
    component2 = Component('M', {'a', 'b'})
    component3 = Component('M', {'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    component4 = Component('M', {'a', 'b'}, {AuxEdge('a', 'b', 'trans')})

    assert component1 == component2
    assert component1 != component3
    assert component3 != component4


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
