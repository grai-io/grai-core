from typing import Union

from grai_schemas.v1 import EdgeV1, NodeV1, WorkspaceV1
from grai_schemas.v1.edge import EdgeIdTypes, EdgeSpec, SourcedEdgeV1
from grai_schemas.v1.node import NodeIdTypes, SourcedNodeSpec, SourcedNodeV1
from grai_schemas.v1.source import SourceSpec, SourceV1

from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.labels import (
    EdgeLabels,
    NodeLabels,
    SourceLabels,
    WorkspaceLabels,
)


@ClientV1.get_url.register
def get_node_url(client: ClientV1, obj: Union[NodeIdTypes, NodeV1, SourcedNodeV1, SourcedNodeSpec, NodeLabels]) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.node_endpoint


@ClientV1.get_url.register
def get_edge_url(client: ClientV1, obj: Union[EdgeV1, EdgeLabels, EdgeIdTypes, EdgeSpec]) -> str:
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
def get_workspace_url(client: ClientV1, obj: Union[WorkspaceLabels, WorkspaceV1]) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.workspace_endpoint


@ClientV1.get_url.register
def get_source_url(client: ClientV1, obj: Union[SourceLabels, SourceV1, SourceSpec]) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return client.source_endpoint
