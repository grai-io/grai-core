from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type

import typer

from grai_cli.api.entrypoint import app
from grai_cli.settings.config import config
from grai_cli.utilities.headers import authenticate
from grai_cli.utilities.utilities import default_callback

if TYPE_CHECKING:
    from grai_client.endpoints.client import BaseClient


def get_default_client() -> BaseClient:
    """

    Args:

    Returns:

    Raises:

    """
    from grai_client.endpoints.v1.client import ClientV1

    _clients: Dict[str, Type[BaseClient]] = {
        "v1": ClientV1,
    }
    host = config.server.host
    port = config.server.port
    workspace = config.server.workspace
    insecure = config.server.insecure

    client = _clients[config.server.api_version](host=host, port=port, workspace=workspace, insecure=insecure)

    authenticate(client)
    return client


client_app = typer.Typer(no_args_is_help=True, help="Interact with The Guide", callback=default_callback)
app.add_typer(client_app, name="client")


client_get_app = typer.Typer(no_args_is_help=True, help="Get objects from The Guide", callback=default_callback)
app.add_typer(client_get_app, name="get")
