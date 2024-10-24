import pytest

from recsa import ComponentStructure, LocalAuxEdge, RecsaValueError


@pytest.fixture
def comp() -> ComponentStructure:
    return ComponentStructure('M', {'a', 'b'})

@pytest.fixture
def comp_with_aux_edges() -> ComponentStructure:
    return ComponentStructure('M', {'a', 'b'}, {LocalAuxEdge('a', 'b', 'cis')})


def test_init_with_valid_args(comp) -> None:
    assert comp.component_kind == 'M'
    assert set(comp.binding_sites) == {'a', 'b'}


def test_init_with_valid_args_with_single_aux_edge(comp_with_aux_edges) -> None:
    assert comp_with_aux_edges.component_kind == 'M'
    assert set(comp_with_aux_edges.binding_sites) == {'a', 'b'}
    assert comp_with_aux_edges.aux_edges == {LocalAuxEdge('a', 'b', 'cis')}


def test_init_with_valid_args_with_multiple_aux_edges() -> None:
    component = ComponentStructure('M', {'a', 'b', 'c'}, {
        LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('a', 'c', 'cis'), 
        LocalAuxEdge('b', 'c', 'trans')})
    
    assert component.kind == 'M'
    assert set(component.binding_sites) == {'a', 'b', 'c'}
    assert component.aux_edges == {
        LocalAuxEdge('a', 'b', 'cis'), LocalAuxEdge('a', 'c', 'cis'), 
        LocalAuxEdge('b', 'c', 'trans')}


def test_init_with_invalid_aux_edge_whose_binding_sites_not_in_binding_sites() -> None:
    with pytest.raises(RecsaValueError):
        ComponentStructure('M', {'a', 'b'}, {LocalAuxEdge('a', 'c', 'cis')})


def test_init_with_empty_binding_sites() -> None:
    # Empty binding sites is allowed.
    component = ComponentStructure('M', set())
    assert component.binding_sites == set()


def test_init_with_empty_aux_edges() -> None:
    # Empty aux_edges is allowed.
    component = ComponentStructure('M', {'a', 'b'}, set())
    assert component.aux_edges == set()


def test_eq() -> None:
    component1 = ComponentStructure('M', {'a', 'b'})
    component2 = ComponentStructure('M', {'a', 'b'})
    component3 = ComponentStructure('M', {'a', 'b'}, {LocalAuxEdge('a', 'b', 'cis')})
    component4 = ComponentStructure('M', {'a', 'b'}, {LocalAuxEdge('a', 'b', 'trans')})

    assert component1 == component2
    assert component1 != component3
    assert component3 != component4


def test_clear_g_cache(comp) -> None:
    comp._Component__g_cache = 1
    assert comp._Component__g_cache == 1

    comp._ComponentStructure__add_binding_site('c')
    assert comp._ComponentStructure__g_cache is None


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
