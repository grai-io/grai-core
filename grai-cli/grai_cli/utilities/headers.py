from grai_cli import config
import requests
from grai_client.authentication import UserTokenHeader, APIKeyHeader, UserNameHeader
import typer
from requests import Response
from typing import Callable, Dict

json_headers = {"accept": "application/json", "Content-Type": "application/json"}

server_configs = config.get(
    {
        "server": {
            "host": str,
            "port": str,
        }
    }
)


def get_jwt(self, username, password):
    response = requests.post(
        f"{self.api}/token/", headers=self.json_headers, params=self.user_auth_params
    )
    if response.status_code != 200:
        raise

    return response.json()


def authenticate_with_username(client):
    username = config.grab("auth.username")
    password = config.grab("auth.password")
    client.set_authentication_headers(username=username, password=password)


def authenticate_with_token(client):
    token = config.grab("auth.token")
    client.set_authentication_headers(token=token)


def authenticate_with_api_key(client):
    api_key = config.grab("auth.api_key")
    client.set_authentication_headers(api_key=api_key)


# TODO Switch to pydantic
def authenticate(client):
    auth_modes = [
        authenticate_with_api_key,
        authenticate_with_token,
        authenticate_with_username,
    ]
    for mode in auth_modes:
        try:
            return mode(client)
        except Exception as e:
            pass

    raise Exception("No supported authentication mode found for your config.")


def response_auth_checker(fn: Callable[[...], Response]) -> Callable[[...], Dict]:
    def response_status_check(resp: Response) -> Response:
        if resp.status_code in {200, 201}:
            return resp
        elif resp.status_code in {400, 401, 402, 403}:
            typer.echo(f"Failed to Authenticate with code: {resp.status_code}")
            raise typer.Exit()
        elif resp.status_code == 404:
            typer.echo(resp.reason)
            raise typer.Exit()
        elif resp.status_code == 415:
            typer.echo(resp.reason)
            raise typer.Exit()
        elif resp.status_code == 500:
            typer.echo(resp.text)
            message = (
                "Hit an internal service error, this looks like a bug, sorry! "
                "Please submit a bug report to https://github.com/grai-io/grai-core/issues"
            )
            typer.echo(message)
            raise typer.Exit()
        else:
            typer.echo(f"No handling for error code {resp.status_code}")
            raise typer.Exit()

    def inner(*args, **kwargs) -> Dict:
        response = response_status_check(fn(*args, **kwargs))
        return response.json()

    return inner
