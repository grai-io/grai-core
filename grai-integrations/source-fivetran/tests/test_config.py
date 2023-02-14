import os

from grai_source_fivetran.loader import FiveTranConfig


def test_load_config_from_env_variables():
    env_vars = {
        "GRAI_FIVETRAN_ENDPOINT": "http://www.fivetran.com",
        "GRAI_FIVETRAN_API_KEY": "test_key",
        "GRAI_FIVETRAN_API_SECRET": "test_secret",
    }
    os.environ.update(env_vars)

    config = FiveTranConfig()
    assert config.endpoint == "http://www.fivetran.com"
    assert config.api_key.get_secret_value() == "test_key"
    assert config.api_secret.get_secret_value() == "test_secret"
    for k, v in env_vars.items():
        os.environ.pop(k)


def test_load_config_arguments():
    config = FiveTranConfig(api_key="test_key", api_secret="test_secret", endpoint="http://www.fivetran.com")
    assert config.endpoint == "http://www.fivetran.com"
    assert config.api_key.get_secret_value() == "test_key"
    assert config.api_secret.get_secret_value() == "test_secret"


def test_config_has_default_endpoint():
    config = FiveTranConfig(api_key="test_key", api_secret="test_secret")
    assert config.endpoint == "https://api.fivetran.com/v1"


def test_config_endpoint_handles_trailing_slash():
    config = FiveTranConfig(
        api_key="test_key",
        api_secret="test_secret",
        endpoint="http://www.fivetran.com/",
    )
    assert config.endpoint == "http://www.fivetran.com"
