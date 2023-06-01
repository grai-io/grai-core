from typing import Sequence, Type

from grai_client.endpoints import client, rest, utilities, v1


def list_clients() -> Sequence[Type[client.BaseClient]]:
    """

    Args:

    Returns:

    Raises:

    """
    clients = [v1.client.ClientV1]
    return clients
