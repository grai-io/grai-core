from grai_schemas.v1 import EdgeV1, NodeV1, WorkspaceV1
from grai_schemas.v1.edge import SourcedEdgeV1
from grai_schemas.v1.node import NodeIdTypes, SourcedNodeV1

from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.labels import EdgeLabels, NodeLabels, WorkspaceLabels


@ClientV1.get_url.register
def get_node_id_url(client: ClientV1, obj: NodeIdTypes) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.node_endpoint


@ClientV1.get_url.register
def get_node_url(client: ClientV1, obj: NodeV1) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.node_endpoint


@ClientV1.get_url.register
def get_sourced_node_url(client: ClientV1, obj: SourcedNodeV1) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return f"{client.node_endpoint}/{obj.spec.data_source.id}/{obj.spec.id}/"


@ClientV1.get_url.register
def get_edge_url(client: ClientV1, obj: EdgeV1) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.edge_endpoint


@ClientV1.get_url.register
def get_sourced_edge_url(client: ClientV1, obj: SourcedEdgeV1) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return f"{client.edge_endpoint}/{obj.spec.data_source}/{obj.spec.id}/"


@ClientV1.get_url.register
def get_node_label_url(client: ClientV1, obj: NodeLabels) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.node_endpoint


@ClientV1.get_url.register
def get_edge_label_url(client: ClientV1, obj: EdgeLabels) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.edge_endpoint


@ClientV1.get_url.register
def get_workspace_label_url(client: ClientV1, obj: WorkspaceLabels) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.workspace_endpoint


@ClientV1.get_url.register
def get_workspace_label_url(client: ClientV1, obj: WorkspaceV1) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.workspace_endpoint
