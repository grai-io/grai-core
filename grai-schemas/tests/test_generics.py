import dataclasses

import pytest
from grai_schemas.generics import DefaultValue, PackageConfig
from pydantic import BaseModel


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


def test_create_default_value_from_parent_class():
    class DefaultTest(BaseModel):
        test: DefaultValue

    result = DefaultTest(test=DefaultValue())
    value = result.test
    assert value.default_value is None
    assert value.has_default_value is None
    assert value.data_type is None


def test_create_default_value_from_parent_class():
    class DefaultTest(BaseModel):
        test: DefaultValue

    result = DefaultTest(test={"has_default_value": False})
    value = result.test
    assert value.default_value is None
    assert value.has_default_value is False
    assert value.data_type is None


@pytest.mark.xfail
def test_incorrectly_initialized_default_value():
    value = DefaultValue(has_default_value=False, default_value=2)


@pytest.mark.xfail
def test_incorrectly_initialized_default_value2():
    value = DefaultValue(has_default_value=None, default_value=2)


@pytest.mark.xfail
def test_config_missing_fields():
    class Config(PackageConfig, BaseModel):
        metadata_id = "test-test"
        integration_name = "test-test"

    conf = Config()
