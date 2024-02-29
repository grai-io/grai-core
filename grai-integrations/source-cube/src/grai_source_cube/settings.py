import datetime
from typing import Optional
from urllib.parse import urlparse, urlunparse

import jwt
from pydantic import (
    AnyUrl,
    BaseSettings,
    PrivateAttr,
    SecretStr,
    root_validator,
    validator,
)


class CubeApiConfig(BaseSettings):
    api_url: AnyUrl
    api_secret: Optional[SecretStr] = None
    api_token: Optional[SecretStr] = None

    _api_jwt_token: Optional[SecretStr] = PrivateAttr(None)
    _jwt_token_expiry: Optional[datetime.datetime] = PrivateAttr(None)

    @validator("api_url")
    def validate_api_url(cls, value):
        """
        This should end in /v1
        Args:
            value:

        Returns:

        Raises:


        """
        url = value.rstrip("/")
        if not url.endswith("/v1"):
            raise ValueError("api_url must end in /v1")
        return url

    @validator("api_token")
    def validate_api_token(cls, value: Optional[SecretStr]):
        """"""
        if value is None:
            return None

        try:
            jwt.decode(value.get_secret_value(), options={"verify_signature": False})
            return value
        except jwt.exceptions.DecodeError:
            raise jwt.exceptions.DecodeError("Provided api_token was not a valid jwt token.")
        except Exception as e:
            raise ValueError("Failed to parse jwt token for unknown reason.") from e

    @root_validator
    def check_for_secret_or_token(cls, values):
        secret, token = values.get("api_secret"), values.get("api_token")

        if secret is None and token is None:
            raise ValueError("The Cube API config requires either an api_secret or a jwt api_token.")
        return values

    @property
    def base_url(self) -> str:
        parsed_url = urlparse(self.api_url)
        base_url = urlunparse((parsed_url.scheme, parsed_url.netloc, "", "", "", ""))
        return base_url

    @property
    def jwt_token(self) -> str:
        if self.api_token is not None:
            return self.api_token.get_secret_value()
        elif self._api_jwt_token is None:
            self.set_jwt_token()
        elif self._jwt_token_expiry and self._jwt_token_expiry < datetime.datetime.now(datetime.UTC):
            self.set_jwt_token()

        token: str = self._api_jwt_token.get_secret_value()  # type: ignore
        return token

    def set_jwt_token(self) -> None:
        expiration_time = datetime.datetime.now(datetime.UTC) + datetime.timedelta(minutes=5)
        payload = {"exp": expiration_time}
        cube_token = jwt.encode(payload, self.api_secret.get_secret_value(), algorithm="HS256")
        self._api_jwt_token = SecretStr(cube_token)
        self._jwt_token_expiry = expiration_time

    class Config:
        """ """

        env_prefix = "grai_cube_"
        env_file = ".env"
