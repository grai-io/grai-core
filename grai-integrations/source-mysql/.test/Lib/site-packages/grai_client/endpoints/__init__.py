from grai_client.endpoints import client, utilities, v1
from typing import List, Type, Sequence


def list_clients() -> Sequence[Type[client.BaseClient]]:
    clients = [v1.client.ClientV1]
    return clients
