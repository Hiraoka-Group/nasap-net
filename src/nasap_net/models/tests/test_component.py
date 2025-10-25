from dataclasses import FrozenInstanceError

import pytest

from nasap_net.models import Component


def test_component():
    M = Component(kind="M", sites=["a", "b"])
    assert M.kind == "M"
    assert M.site_ids == frozenset({"a", "b"})


def test_component_immutability():
    M = Component(kind="M", sites=["a", "b"])
    with pytest.raises(FrozenInstanceError):
        M.kind = "M2"
    with pytest.raises(FrozenInstanceError):
        M.site_ids = frozenset({"c"})
