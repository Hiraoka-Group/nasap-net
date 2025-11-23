from nasap_net.utils import default_if_none

def test_default_if_none_with_value():
    value = 42
    default = 100
    result = default_if_none(value, default)
    assert result == value


def test_default_if_none_with_none():
    value = None
    default = 100
    result = default_if_none(value, default)
    assert result == default


def test_default_if_none_with_string_value():
    value = "hello"
    default = "world"
    result = default_if_none(value, default)
    assert result == value


def test_default_if_none_with_string_none():
    value = None
    default = "world"
    result = default_if_none(value, default)
    assert result == default
