from typing import Optional

from grai_schemas.v1 import EdgeV1, NodeV1, WorkspaceV1
from grai_schemas.v1.edge import SourcedEdgeV1
from grai_schemas.v1.node import SourcedNodeV1

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get, post
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.utils import process_node_id


@post.register
def post_node_v1(client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()) -> NodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    response = post(client, url, grai_type.spec.dict(exclude_none=True), options=options)
    return NodeV1.from_spec(response.json())


@post.register
def post_sourced_node_v1(
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
    url = client.get_url(grai_type)
    response = post(client, url, grai_type.spec.dict(exclude_none=True), options=options)
    return SourcedNodeV1.from_spec(response.json())


@post.register
def post_edge_v1(client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()) -> Optional[EdgeV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    # source, destination = asyncio.gather(
    #     process_node_id(client, grai_type.spec.source, options),
    #     process_node_id(client, grai_type.spec.destination, options),
    # )

    payload = grai_type.spec.dict(exclude_none=True)

    response = post(client, url, payload, options=options)
    response = response.json()

    if response is None:
        return None

    response["source"] = {**payload["source"], "id": response["source"]}
    response["destination"] = {**payload["destination"], "id": response["destination"]}

    return EdgeV1.from_spec(response)


@post.register
def post_workspace_v1(
    client: ClientV1, grai_type: WorkspaceV1, options: ClientOptions = ClientOptions()
) -> WorkspaceV1:
    """
    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:
    """
    url = client.get_url(grai_type)
    payload = grai_type.spec.dict(exclude_none=True)
    response = post(client, url, payload, options=options)
    return WorkspaceV1.from_spec(response.json())
