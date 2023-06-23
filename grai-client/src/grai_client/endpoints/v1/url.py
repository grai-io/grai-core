from typing import Union
from uuid import UUID

from grai_schemas.v1 import EdgeV1, NodeV1, WorkspaceV1
from grai_schemas.v1.edge import EdgeIdTypes, EdgeSpec, SourcedEdgeV1
from grai_schemas.v1.node import NodeIdTypes, SourcedNodeSpec, SourcedNodeV1
from grai_schemas.v1.source import SourceSpec, SourceV1

from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.labels import (
    EdgeLabels,
    NodeLabels,
    SourceEdgeLabels,
    SourceLabels,
    SourceNodeLabels,
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
    return client.source_endpoint


@ClientV1.get_url.register
def get_sourced_node_url(
    client: ClientV1, type_identifier: Union[SourceNodeLabels, SourcedNodeV1, SourcedNodeSpec], source_id: UUID
) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return f"{client.source_endpoint}{source_id}/nodes/"


@ClientV1.get_url.register
def get_sourced_node_spec_url(
    client: ClientV1,
    type_identifier: Union[SourceNodeLabels, SourcedNodeV1, SourcedNodeSpec],
    source_id: UUID,
    node_id: UUID,
) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return f"{client.get_url(type_identifier, source_id)}{node_id}/"


@ClientV1.get_url.register
def get_sourced_edge_url(client: ClientV1, type_identifier: SourceEdgeLabels, source_id: UUID) -> str:
    """

    Args:
        client:
        obj:

    Returns:

    Raises:

    """
    return f"{client.source_endpoint}{source_id}/edges/"


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
