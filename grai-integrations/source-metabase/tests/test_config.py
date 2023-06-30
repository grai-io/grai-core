import os

from src.grai_source_metabase.loader import MetabaseConfig


def test_load_config_from_env_variables():
    """ """
    env_vars = {
        "GRAI_METABASE_USERNAME": "test_user",
        "GRAI_METABASE_PASSWORD": "test_password",
        "GRAI_METABASE_ENDPOINT": "https://data.inv.tech/api",
    }
    os.environ.update(env_vars)

    config = MetabaseConfig()
    assert config.username.get_secret_value() == "test_user"
    assert config.password.get_secret_value() == "test_password"
    assert config.endpoint == "https://data.inv.tech/api"
    for k, v in env_vars.items():
        os.environ.pop(k)


def test_load_config_arguments():
    """ """
    config = MetabaseConfig(
        username="test_user",
        password="test_password",
        endpoint="https://data.inv.tech/api",
    )
    assert config.username.get_secret_value() == "test_user"
    assert config.password.get_secret_value() == "test_password"
    assert config.endpoint == "https://data.inv.tech/api"


def test_config_has_default_endpoint():
    """ """
    config = MetabaseConfig(username="test_user", password="test_password")
    assert config.endpoint == "https://data.inv.tech/api"


def test_config_endpoint_handles_trailing_slash():
    """ """
    config = MetabaseConfig(
        username="test_user",
        password="test_password",
        endpoint="https://data.inv.tech/api/",
    )
    assert config.endpoint == "https://data.inv.tech/api"
