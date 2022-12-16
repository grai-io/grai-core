from grai_client.endpoints.v1.utils import process_node_id
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1


@ClientV1.post.register
def post_node_v1(client: ClientV1, grai_type: NodeV1) -> NodeV1:
    url = client.get_url(grai_type)
    response = client.post(url, grai_type.spec.dict(exclude_none=True))
    return NodeV1.from_spec(response.json())


@ClientV1.post.register
def post_edge_v1(client: ClientV1, grai_type: EdgeV1) -> EdgeV1:
    url = client.get_url(grai_type)

    source = process_node_id(client, grai_type.spec.source)
    destination = process_node_id(client, grai_type.spec.destination)

    payload = grai_type.spec.dict(exclude_none=True)
    payload["source"] = source.id
    payload["destination"] = destination.id
    response = client.post(url, payload).json()

    if response is None:
        return None

    response["source"] = source
    response["destination"] = destination
    return EdgeV1.from_spec(response)

