from typing import Dict, Type

import typer
from grai_client.endpoints.client import BaseClient

from grai_cli.api.entrypoint import app
from grai_cli.settings.config import config
from grai_cli.utilities.headers import authenticate

# def get_cli_client(client: Type[BaseClient]):
#     class VersionedCLIClient(client):
#         def __getattr__(self, attr):
#             try:
#                 return getattr(super(), attr)
#             except:
#                 print(f"Exiting with error, client has no attribute {attr}")
#                 typer.Exit()
#
#     return VersionedCLIClient


def get_default_client() -> BaseClient:
    from grai_client.endpoints.v1.client import ClientV1

    _clients: Dict[str, Type[BaseClient]] = {
        "v1": ClientV1,
    }
    host = config.grab("server.host")
    port = config.grab("server.port")
    client = _clients[config.grab("server.api_version")](host, port)
    authenticate(client)
    return client


client_app = typer.Typer(no_args_is_help=True, help="Interact with The Guide")
app.add_typer(client_app, name="client")


client_get_app = typer.Typer(no_args_is_help=True, help="Get objects from The Guide")
app.add_typer(client_get_app, name="get")
