import pytest
from grai_schemas.generics import DefaultValue


def test_default_value_with_no_args():
    value = DefaultValue()
    assert value.default_value is None
    assert value.has_default_value is None
    assert value.data_type is None


def test_create_default_value():
    value = DefaultValue(has_default_value=True, default_value=2, data_type="int")
    assert value.default_value == 2
    assert value.has_default_value is True
    assert value.data_type == "int"


@pytest.mark.xfail
def test_incorrectly_initialized_default_value():
    value = DefaultValue(has_default_value=False, default_value=2)


@pytest.mark.xfail
def test_incorrectly_initialized_default_value2():
    value = DefaultValue(has_default_value=None, default_value=2)
