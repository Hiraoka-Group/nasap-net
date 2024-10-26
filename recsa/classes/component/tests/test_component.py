import pytest

import recsa as rx
from recsa import AuxEdge, Component


def test_typical_usage():
    bindsites = ['a', 'b', 'c', 'd']
    aux_edges = [('a', 'b', 'cis'), ('b', 'c', 'cis'),
                 ('c', 'd', 'cis'), ('d', 'a', 'cis')]
    M = Component(bindsites, aux_edges)
    assert M.bindsites == set(bindsites)
    assert M.aux_edges == {AuxEdge(*edge) for edge in aux_edges}


def test_init():
    bindsites = {'a', 'b'}
    M = Component(bindsites)
    assert M.bindsites == bindsites
    assert M.aux_edges == set()


def test_init_with_bindsites_of_type_tuple():
    bindsites = ['a', 'b']
    M = Component(bindsites)
    assert M.bindsites == set(bindsites)
    assert M.aux_edges == set()


def test_init_with_aux_edges():
    bindsites = {'a', 'b'}
    aux_edges = {AuxEdge('a', 'b', 'cis')}
    M = Component(bindsites, aux_edges)
    assert M.bindsites == bindsites
    assert M.aux_edges == aux_edges


def test_init_with_aux_edges_of_type_tuple():
    bindsites = {'a', 'b'}
    aux_edges = [('a', 'b', 'cis')]
    M = Component(bindsites, aux_edges)
    assert M.bindsites == bindsites
    assert M.aux_edges == {AuxEdge(*edge) for edge in aux_edges}


def test_init_with_empty_binding_sites():
    # Raises no error.
    M = Component(set())
    assert M.bindsites == set()


def test_init_with_empty_aux_edges():
    # Raises no error.
    M = Component({'a', 'b'}, set())
    assert M.aux_edges == set()


def test_init_with_invalid_aux_edge():
    with pytest.raises(rx.RecsaValueError):
        # The binding site 'c' is not in the binding sites.
        Component({'a', 'b'}, {AuxEdge('a', 'c', 'cis')})


def test_eq():
    M1 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    M2 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    assert M1 == M2


def test_eq_with_different_binding_sites():
    M1 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    M2 = Component({'a', 'c'}, {AuxEdge('a', 'c', 'cis')})
    assert M1 != M2


def test_eq_with_different_aux_edges():
    M1 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'cis')})
    M2 = Component({'a', 'b'}, {AuxEdge('a', 'b', 'trans')})
    assert M1 != M2


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
