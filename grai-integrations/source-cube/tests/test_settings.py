import jwt
from grai_source_cube.settings import CubeApiConfig
from pydantic import SecretStr

TEST_TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJleHAiOjE3MDg0NjEyMTZ9.ry6TdZBuAGmrWDWvoTSs7GhjVXbcNC8-QTXi_FEbHQk"


def test_load_config_token_from_env_variables(monkeypatch):
    """ """
    monkeypatch.setenv("GRAI_CUBE_API_URL", "https://www.cube.dev/cubejs-api/v1")
    monkeypatch.setenv("GRAI_CUBE_API_TOKEN", TEST_TOKEN)

    config = CubeApiConfig()
    assert config.api_url == "https://www.cube.dev/cubejs-api/v1"
    assert config.api_token.get_secret_value() == TEST_TOKEN
    assert config.api_secret is None


def test_load_config_secret_from_env_variables(monkeypatch):
    """ """
    monkeypatch.setenv("GRAI_CUBE_API_URL", "https://www.cube.dev/cubejs-api/v1")
    monkeypatch.setenv("GRAI_CUBE_API_SECRET", "test_secret")

    config = CubeApiConfig()
    assert config.api_url == "https://www.cube.dev/cubejs-api/v1"
    assert isinstance(config.api_secret, SecretStr)
    assert config.api_secret.get_secret_value() == "test_secret"


def test_secret_config_has_valid_token(monkeypatch):
    """ """
    monkeypatch.setenv("GRAI_CUBE_API_URL", "https://www.cube.dev/cubejs-api/v1")
    monkeypatch.setenv("GRAI_CUBE_API_SECRET", "test_secret")

    config = CubeApiConfig()

    assert config.jwt_token is not None
    jwt.decode(config.jwt_token, "test_secret", algorithms=["HS256"])


def test_load_config_arguments():
    """ """
    config = CubeApiConfig(api_token=TEST_TOKEN, api_url="https://www.cube.dev/cubejs-api/v1")
    assert config.api_url == "https://www.cube.dev/cubejs-api/v1"
    assert config.api_token.get_secret_value() == TEST_TOKEN
    assert config.api_secret is None


def test_correct_base_url():
    """ """
    config = CubeApiConfig(api_token=TEST_TOKEN, api_url="https://www.cube.dev/cubejs-api/v1")
    assert config.base_url == "https://www.cube.dev"


def test_config_endpoint_handles_trailing_slash():
    """ """
    config = CubeApiConfig(
        api_token=TEST_TOKEN,
        api_url="https://www.cube.dev/stuff/v1/",
    )
    assert config.api_token.get_secret_value() == TEST_TOKEN
    assert config.api_url == "https://www.cube.dev/stuff/v1"
