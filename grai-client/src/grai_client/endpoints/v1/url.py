from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.node import NodeIdTypes

from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.labels import EdgeLabels, NodeLabels, WorkspaceLabels


@ClientV1.get_url.register
def get_node_id_url(client: ClientV1, obj: NodeIdTypes) -> str:
    """

    Args:
        client (ClientV1):
        obj (NodeIdTypes):

    Returns:

    Raises:

    """
    return client.node_endpoint


@ClientV1.get_url.register
def get_node_url(client: ClientV1, obj: NodeV1) -> str:
    """

    Args:
        client (ClientV1):
        obj (NodeV1):

    Returns:

    Raises:

    """
    return client.node_endpoint


@ClientV1.get_url.register
def get_edge_url(client: ClientV1, obj: EdgeV1) -> str:
    """

    Args:
        client (ClientV1):
        obj (EdgeV1):

    Returns:

    Raises:

    """
    return client.edge_endpoint


@ClientV1.get_url.register
def get_node_label_url(client: ClientV1, obj: NodeLabels) -> str:
    """

    Args:
        client (ClientV1):
        obj (NodeLabels):

    Returns:

    Raises:

    """
    return client.node_endpoint


@ClientV1.get_url.register
def get_edge_label_url(client: ClientV1, obj: EdgeLabels) -> str:
    """

    Args:
        client (ClientV1):
        obj (EdgeLabels):

    Returns:

    Raises:

    """
    return client.edge_endpoint


@ClientV1.get_url.register
def get_workspace_label_url(client: ClientV1, obj: WorkspaceLabels) -> str:
    """

    Args:
        client (ClientV1):
        obj (WorkspaceLabels):

    Returns:

    Raises:

    """
    return client.workspace_endpoint
