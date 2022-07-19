import typer
from requests import Response
from typing import Callable, Dict


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
            message = ("Hit an internal service error, this looks like a bug, sorry! "
                       "Please submit a bug report to https://github.com/grai-io/grai-core/issues")
            typer.echo(message)
            raise typer.Exit()
        else:
            typer.echo(f"No handling for error code {resp.status_code}")
            raise typer.Exit()

    def inner(*args, **kwargs) -> Dict:
        response = response_status_check(fn(*args, **kwargs))
        return response.json()

    return inner

