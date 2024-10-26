import pytest

from recsa import AuxEdge, Component, RecsaValueError


@pytest.fixture
def comp() -> Component:
    return Component({'a', 'b'})

@pytest.fixture
def comp_with_aux_edges() -> Component:
    return Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})


def test_init_with_valid_args(comp) -> None:
    assert set(comp.binding_sites) == {'a', 'b'}


def test_init_with_valid_args_with_single_aux_edge(comp_with_aux_edges) -> None:
    assert set(comp_with_aux_edges.binding_sites) == {'a', 'b'}
    assert comp_with_aux_edges.aux_edges == {AuxEdge('a', 'b', 'cis')}


def test_init_with_valid_args_with_multiple_aux_edges() -> None:
    component = Component({'a', 'b', 'c'}, {
        AuxEdge('a', 'b', 'cis'), AuxEdge('a', 'c', 'cis'), 
        AuxEdge('b', 'c', 'trans')})
    
    assert set(component.binding_sites) == {'a', 'b', 'c'}
    assert component.aux_edges == {
        AuxEdge('a', 'b', 'cis'), AuxEdge('a', 'c', 'cis'), 
        AuxEdge('b', 'c', 'trans')}


def test_init_with_invalid_aux_edge_whose_binding_sites_not_in_binding_sites() -> None:
    with pytest.raises(RecsaValueError):
        Component({'a', 'b'}, {AuxEdge('a', 'c', 'cis')})


def test_init_with_empty_binding_sites() -> None:
    # Empty binding sites is allowed.
    component = Component(set())
    assert component.binding_sites == set()


def test_init_with_empty_aux_edges() -> None:
    # Empty aux_edges is allowed.
    component = Component({'a', 'b'}, set())
    assert component.aux_edges == set()


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
