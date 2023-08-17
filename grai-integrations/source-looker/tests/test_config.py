import os

from grai_source_looker.loader import LookerConfig


def test_load_config_from_env_variables():
    """ """
    env_vars = {
        "GRAI_LOOKER_BASE_URL": "http://my.looker.com",
        "GRAI_LOOKER_CLIENT_ID": "test_key",
        "GRAI_LOOKER_CLIENT_SECRET": "test_secret",
        "GRAI_LOOKER_VERIFY_SSL": "True",
        "GRAI_LOOKER_NAMESPACE": "test",
    }
    os.environ.update(env_vars)

    config = LookerConfig()
    assert config.base_url == "http://my.looker.com"
    assert config.client_id == "test_key"
    assert config.client_secret.get_secret_value() == "test_secret"
    assert config.verify_ssl == True
    assert config.namespace == "test"
    for k, v in env_vars.items():
        os.environ.pop(k)


def test_load_config_arguments(loader_kwargs):
    """ """
    config = LookerConfig(**loader_kwargs)
    for k, v in loader_kwargs.items():
        if k == "client_secret":
            assert config.client_secret.get_secret_value() == v
        else:
            assert getattr(config, k) == v


def test_config_base_url_validation(loader_kwargs):
    config_kwargs = loader_kwargs.copy()
    config_kwargs["base_url"] = "http://my.looker.com/api/.../asd/?as=true"
    config = LookerConfig(**config_kwargs)
    assert config.base_url == "http://my.looker.com"
