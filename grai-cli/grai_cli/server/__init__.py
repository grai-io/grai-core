from grai_cli.server import utilities
from grai_cli.server import authenticate
from grai_cli.server import endpoints
from grai_cli import config
from grai_cli.server.endpoints.client import BaseClient
from typing import Type, Dict


def get_default_client() -> BaseClient:
    from grai_cli.server.endpoints.v1.client import ClientV1

    _clients: Dict[str, Type[BaseClient]] = {
        'v1': ClientV1
    }
    return _clients[config.grab('server.api_version')]()
