from typing import Optional, TypeVar, Union

from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1, SourceV1
from grai_schemas.v1.node import SourcedNodeSpec
from grai_schemas.v1.organization import OrganisationSpec, OrganisationV1
from grai_schemas.v1.workspace import WorkspaceSpec, WorkspaceV1

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get, patch
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.get.node import get_source_and_node_spec
from grai_client.errors import NotSupportedError

T = TypeVar("T", NodeV1, EdgeV1)


@patch.register
def patch_node_v1(client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()) -> NodeV1:
    """

    Args:
        client (ClientV1):
        grai_type (NodeV1):
        options (ClientOptions, optional):  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.spec.id is None:
        current = get(client, grai_type)
        grai_type.spec.id = current.spec.id
    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    response = patch(client, url, grai_type.spec.dict(exclude_none=True), options=options).json()
    return NodeV1.from_spec(response)


@patch.register
def patch_sourced_node_v1(
    client: ClientV1, grai_type: SourcedNodeV1, options: ClientOptions = ClientOptions()
) -> SourcedNodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """

    return patch(client, grai_type.spec, options)


@patch.register
def patch_sourced_node_spec(
    client: ClientV1, grai_type: SourcedNodeSpec, options: ClientOptions = ClientOptions()
) -> SourcedNodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    source, node = get_source_and_node_spec(client, grai_type)

    url = client.get_url(grai_type, source.id, node.id)
    response = patch(client, url, grai_type.dict(exclude_none=True), options=options).json()
    response["data_source"] = source
    return SourcedNodeV1.from_spec(response)


@patch.register
def patch_edge_v1(client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()) -> EdgeV1:
    """

    Args:
        client (ClientV1):
        grai_type (EdgeV1):
        options (ClientOptions, optional):  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.spec.id is None:
        current = get(client, grai_type)
        grai_type.spec.id = current.spec.id

    payload = grai_type.spec.dict(exclude_none=True)

    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    response = patch(client, url, payload, options=options)
    response = response.json()

    response["source"] = {**payload["source"], "id": response["source"]}
    response["destination"] = {**payload["destination"], "id": response["destination"]}
    return EdgeV1.from_spec(response)


@patch.register
def patch_workspace_v1(
    client: ClientV1, grai_type: Union[WorkspaceV1, WorkspaceSpec], options: ClientOptions = ClientOptions()
):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    message = "The patch workspace endpoint is not supported through the REST API."
    raise NotSupportedError(message)


@patch.register
def patch_organisation_v1(
    client: ClientV1, grai_type: Union[OrganisationV1, OrganisationSpec], options: ClientOptions = ClientOptions()
):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    message = "The patch organisation endpoint is not supported through the REST API."
    raise NotSupportedError(message)


@patch.register
def patch_source_v1(client: ClientV1, grai_type: SourceV1, options: ClientOptions = ClientOptions()) -> SourceV1:
    """

    Args:
        client (ClientV1):
        grai_type (NodeV1):
        options (ClientOptions, optional):  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.spec.id is None:
        current = get(client, grai_type)
        grai_type.spec.id = current.spec.id

    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"

    response = patch(client, url, grai_type.spec.dict(exclude_none=True), options=options)
    response = response.json()
    response["workspace"] = client.workspace
    return SourceV1.from_spec(response)
