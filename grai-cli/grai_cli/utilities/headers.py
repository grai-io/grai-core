from __future__ import annotations

from typing import TYPE_CHECKING, Dict

from grai_cli.settings.config import config

if TYPE_CHECKING:
    from grai_client.endpoints.client import BaseClient

json_headers = {"accept": "application/json", "Content-Type": "application/json"}


def get_jwt(self, username: str, password: str) -> Dict:
    import requests

    response = requests.post(
        f"{self.api}/token/", headers=self.json_headers, params=self.user_auth_params
    )
    if response.status_code != 200:
        raise

    return response.json()


def authenticate_with_username(client: BaseClient) -> BaseClient:
    username = config.grab("auth.username")
    password = config.grab("auth.password")
    client.set_authentication_headers(username=username, password=password)
    return client


def authenticate_with_token(client: BaseClient) -> BaseClient:
    token = config.grab("auth.token")
    client.set_authentication_headers(token=token)
    return client


def authenticate_with_api_key(client: BaseClient) -> BaseClient:
    api_key = config.grab("auth.api_key")
    client.set_authentication_headers(api_key=api_key)
    return client


# TODO Switch to pydantic
def authenticate(client: BaseClient) -> BaseClient:
    auth_modes = {
        "username": authenticate_with_username,
        "token": authenticate_with_token,
        "api_key": authenticate_with_api_key,
    }

    auth_mode_id = config.grab("auth.authentication_mode")
    auth_mode = auth_modes[auth_mode_id]
    client = auth_mode(client)
    return client
