import pytest

from recsa.classes.naming_rule import NamingRule


def test_local_to_global():
    naming_rule = NamingRule()
    result = naming_rule.local_to_global('M1', 'a')
    assert result == 'M1.a'


def test_global_to_local():
    naming_rule = NamingRule()
    result = naming_rule.global_to_local('M1.a')
    assert result == ('M1', 'a')


def test_global_to_local_invalid_format():
    naming_rule = NamingRule()
    with pytest.raises(AssertionError):
        naming_rule.global_to_local('invalid_format')


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
