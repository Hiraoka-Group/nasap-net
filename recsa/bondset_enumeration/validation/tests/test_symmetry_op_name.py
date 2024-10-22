import pytest

from recsa import RecsaValueError
from recsa.bondset_enumeration import validate_symmetry_op_name


def test_validate_symmetry_op_name_valid():
    validate_symmetry_op_name('1')   # No error should be raised
    validate_symmetry_op_name('Op_1-1')  # No error should be raised


def test_validate_symmetry_op_name_empty():
    with pytest.raises(RecsaValueError, match='Empty symmetry operation name'):
        validate_symmetry_op_name('')  # empty string


def test_validate_symmetry_op_name_invalid():
    with pytest.raises(RecsaValueError, match='Invalid symmetry operation name'):
        validate_symmetry_op_name('1 2')  # contains a whitespace
    with pytest.raises(RecsaValueError, match='Invalid symmetry operation name'):
        validate_symmetry_op_name('1,2')  # contains a comma
    with pytest.raises(RecsaValueError, match='Invalid symmetry operation name'):
        validate_symmetry_op_name('1:2')  # contains a colon
    with pytest.raises(RecsaValueError, match='Invalid symmetry operation name'):
        validate_symmetry_op_name(' ')  # whitespace only
    with pytest.raises(RecsaValueError, match='Invalid symmetry operation name'):
        validate_symmetry_op_name('結合')  # non-alphanumeric character


if __name__ == '__main__':
    pytest.main(['-vv', __file__])
