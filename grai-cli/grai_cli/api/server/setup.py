from __future__ import annotations

from typing import TYPE_CHECKING, Dict, Type

import typer

from grai_cli.api.callbacks import requires_config_callback
from grai_cli.api.entrypoint import app
from grai_cli.settings.config import config
from grai_cli.utilities.headers import authenticate

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
    url = str(config.server.url)
    workspace = config.server.workspace

    client = _clients[config.server.api_version](url=url, workspace=workspace)
    authenticate(client)

    return client


client_app = typer.Typer(no_args_is_help=True, help="Interact with The Guide", callback=requires_config_callback)


client_get_app = typer.Typer(no_args_is_help=True, help="Get objects from The Guide", callback=requires_config_callback)
