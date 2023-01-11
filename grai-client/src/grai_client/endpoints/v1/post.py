from typing import Optional

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import post
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.utils import process_node_id
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1


@post.register
def post_node_v1(
    client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()
) -> NodeV1:
    url = client.get_url(grai_type)
    response = client.post(url, grai_type.spec.dict(exclude_none=True), options=options)
    return NodeV1.from_spec(response.json())


@post.register
def post_edge_v1(
    client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]:
    url = client.get_url(grai_type)

    source = process_node_id(client, grai_type.spec.source)
    destination = process_node_id(client, grai_type.spec.destination)

    payload = grai_type.spec.dict(exclude_none=True)
    payload["source"] = source.id
    payload["destination"] = destination.id
    response = client.post(url, payload, options=options).json()

    if response is None:
        return None

    response["source"] = source
    response["destination"] = destination
    return EdgeV1.from_spec(response)
