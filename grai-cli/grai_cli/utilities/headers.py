from typing import Dict

import requests
from grai_client.endpoints.client import BaseClient

from grai_cli.settings.config import config

json_headers = {"accept": "application/json", "Content-Type": "application/json"}

server_configs = config.get(
    {
        "server": {
            "host": str,
            "port": str,
        }
    }
)


def get_jwt(self, username: str, password: str) -> Dict:
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


# def response_auth_checker(fn: Callable[[...], Response]) -> Callable[[...], Dict]:
#     def response_status_check(resp: Response) -> Response:
#         if resp.status_code in {200, 201}:
#             return resp
#         elif resp.status_code in {400, 401, 402, 403}:
#             typer.echo(f"Failed to Authenticate with code: {resp.status_code}")
#             raise typer.Exit()
#         elif resp.status_code == 404:
#             typer.echo(resp.reason)
#             raise typer.Exit()
#         elif resp.status_code == 415:
#             typer.echo(resp.reason)
#             raise typer.Exit()
#         elif resp.status_code == 500:
#             typer.echo(resp.text)
#             message = (
#                 "Hit an internal service error, this looks like a bug, sorry! "
#                 "Please submit a bug report to https://github.com/grai-io/grai-core/issues"
#             )
#             typer.echo(message)
#             raise typer.Exit()
#         else:
#             typer.echo(f"No handling for error code {resp.status_code}")
#             raise typer.Exit()
#
#     def inner(*args, **kwargs) -> Dict:
#         response = response_status_check(fn(*args, **kwargs))
#         return response.json()
#
#     return inner
