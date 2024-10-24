import pytest

from recsa.classes.bindsite import BindSite
from recsa.classes.bindsite_id_converter import BindsiteIdConverter


def test_bindsite_initialization():
    bindsite = BindSite('a', 'M1')
    assert bindsite.local == 'a'
    assert bindsite.comp_id == 'M1'


def test_bindsite_initialization_without_comp_id():
    bindsite = BindSite('a')
    assert bindsite.local == 'a'
    assert bindsite.comp_id is None


def test_bindsite_equality():
    bindsite1 = BindSite('a', 'M1')
    bindsite2 = BindSite('a', 'M1')
    bindsite3 = BindSite('b', 'M1')
    assert bindsite1 == bindsite2
    assert bindsite1 != bindsite3


def test_bindsite_hash():
    bindsite1 = BindSite('a', 'M1')
    bindsite2 = BindSite('a', 'M1')
    assert hash(bindsite1) == hash(bindsite2)


def test_bindsite_global():
    bindsite = BindSite('a', 'M1')
    id_converter = BindsiteIdConverter()
    expected_global = id_converter.local_to_global('M1', 'a')
    assert bindsite.global_ == expected_global


def test_bindsite_with_comp_id():
    bindsite = BindSite('a')
    new_bindsite = bindsite.with_comp_id('M2')
    assert new_bindsite.comp_id == 'M2'
    assert new_bindsite.local == 'a'


def test_bindsite_with_comp_id_overwrite():
    bindsite = BindSite('a', 'M1')
    new_bindsite = bindsite.with_comp_id('M2')
    assert new_bindsite.comp_id == 'M2'
    assert new_bindsite.local == 'a'


def test_bindsite_from_global():
    id_converter = BindsiteIdConverter()
    global_id = id_converter.local_to_global('M1', 'a')
    bindsite = BindSite.from_global(global_id)
    assert bindsite.local == 'a'
    assert bindsite.comp_id == 'M1'


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
