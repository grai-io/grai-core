from pydantic import BaseSettings, SecretStr, validator


class CubeApiConfig(BaseSettings):
    """ """

    endpoint: str
    api_token: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, value):
        """

        Args:
            value:

        Returns:

        Raises:

        """
        return value.rstrip("/")

    class Config:
        """ """

        env_prefix = "grai_cube_"
        env_file = ".env"


class CubeConfig(CubeApiConfig):
    namespace: dict
