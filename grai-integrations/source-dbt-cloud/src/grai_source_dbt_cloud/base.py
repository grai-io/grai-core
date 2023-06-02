from typing import List, Optional, Tuple

from grai_client.endpoints.client import BaseClient
from grai_client.update import update
from grai_schemas.base import Edge, Node
from grai_source_dbt_cloud.loader import DbtCloudConnector

from grai_source_dbt.adapters import adapt_to_client


def get_events(connector: DbtCloudConnector, last_event_date: Optional[str]):
    """

    Args:
        connector (DbtCloudConnector):
        last_event_date (Optional[str]):

    Returns:

    Raises:

    """
    events = connector.get_events(last_event_date=last_event_date)

    return events


def get_nodes_and_edges(connector: DbtCloudConnector, version: str = "v1") -> Tuple[List[Node], List[Edge]]:
    """

    Args:
        connector (DbtCloudConnector):
        version (str, optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    nodes, edges = connector.get_nodes_and_edges()

    return nodes, edges


def update_server(client: BaseClient, api_key: str, namespace: str = "default") -> None:
    """

    Args:
        client (BaseClient):
        api_key (str):
        namespace (str, optional):  (Default value = "default")

    Returns:

    Raises:

    """
    conn = DbtCloudConnector(
        namespace=namespace,
        api_key=api_key,
    )
    nodes, edges = get_nodes_and_edges(conn, client.id)

    update(client, nodes)
    update(client, edges)
