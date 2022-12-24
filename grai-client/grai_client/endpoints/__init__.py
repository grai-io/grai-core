from typing import Sequence, Type

from grai_client.endpoints import utilities, rest, client, v1


def list_clients() -> Sequence[Type[client.BaseClient]]:
    clients = [v1.client.ClientV1]
    return clients
