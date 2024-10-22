import pytest

import recsa as rx
from recsa import LocalAuxEdge


def test_LocalAuxEdge_initialization():
    edge = LocalAuxEdge('site1', 'site2', 'cis')
    assert edge.local_bindsite1 == 'site1'
    assert edge.local_bindsite2 == 'site2'
    assert edge.aux_kind == 'cis'


def test_LocalAuxEdge_same_binding_sites():
    with pytest.raises(rx.RecsaValueError):
        LocalAuxEdge('site1', 'site1', 'cis')


def test_LocalAuxEdge_equality():
    edge1 = LocalAuxEdge('site1', 'site2', 'cis')
    edge2 = LocalAuxEdge('site2', 'site1', 'cis')
    assert edge1 == edge2


def test_LocalAuxEdge_inequality():
    edge1 = LocalAuxEdge('site1', 'site2', 'cis')
    edge2 = LocalAuxEdge('site1', 'site3', 'cis')
    assert edge1 != edge2


def test_LocalAuxEdge_hash():
    edge1 = LocalAuxEdge('site1', 'site2', 'cis')
    edge2 = LocalAuxEdge('site2', 'site1', 'cis')
    assert hash(edge1) == hash(edge2)


def test_LocalAuxEdge_repr():
    edge = LocalAuxEdge('site1', 'site2', 'cis')
    assert repr(edge) == "LocalAuxEdge('site1', 'site2', 'cis')"


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
