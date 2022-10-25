from typing import List, Sequence, Type

from grai_client.endpoints import client, utilities, v1


def list_clients() -> Sequence[Type[client.BaseClient]]:
    clients = [v1.client.ClientV1]
    return clients
