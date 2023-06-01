from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from grai_cli.settings.config import config

if TYPE_CHECKING:
    from grai_client.endpoints.client import BaseClient

json_headers = {"accept": "application/json", "Content-Type": "application/json"}


def get_jwt(self, username: str, password: str) -> Dict:
    """

    Args:
        username (str):
        password (str):

    Returns:

    Raises:

    """
    import requests

    response = requests.post(f"{self.api}/token/", headers=self.json_headers, params=self.user_auth_params)
    if response.status_code != 200:
        raise

    return response.json()


def authenticate_with_username(client: BaseClient) -> BaseClient:
    """

    Args:
        client (BaseClient):

    Returns:

    Raises:

    """
    client.authenticate(username=config.auth.username, password=config.auth.password.get_secret_value())
    return client


def authenticate_with_api_key(client: BaseClient) -> BaseClient:
    """

    Args:
        client (BaseClient):

    Returns:

    Raises:

    """
    client.authenticate(api_key=config.auth.api_key.get_secret_value())
    return client


# TODO Switch to pydantic
def authenticate(client: BaseClient) -> BaseClient:
    """

    Args:
        client (BaseClient):

    Returns:

    Raises:

    """
    auth_modes = {
        "username": authenticate_with_username,
        "api_key": authenticate_with_api_key,
    }

    auth_mode_id = config.auth.authentication_mode
    auth_mode = auth_modes[auth_mode_id]
    client = auth_mode(client)
    return client
