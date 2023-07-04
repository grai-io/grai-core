import os

from grai_source_metabase.loader import MetabaseConfig


def test_load_config_from_env_variables():
    env_vars = {
        "GRAI_METABASE_USERNAME": "test_user",
        "GRAI_METABASE_PASSWORD": "test_password",
        "GRAI_METABASE_ENDPOINT": "https://my.super.metabase/api",
    }
    os.environ.update(env_vars)

    config = MetabaseConfig()
    assert config.username.get_secret_value() == "test_user"
    assert config.password.get_secret_value() == "test_password"
    assert config.endpoint == "https://my.super.metabase/api"
    for k, v in env_vars.items():
        os.environ.pop(k)


def test_load_config_arguments():
    config = MetabaseConfig(
        username="test_user",
        password="test_password",
        endpoint="https://my.super.metabase/api",
    )
    assert config.username.get_secret_value() == "test_user"
    assert config.password.get_secret_value() == "test_password"
    assert config.endpoint == "https://my.super.metabase/api"

def test_config_endpoint_handles_trailing_slash():
    config = MetabaseConfig(
        username="test_user",
        password="test_password",
        endpoint="https://my.super.metabase/api/",
    )
    assert config.endpoint == "https://my.super.metabase/api"
