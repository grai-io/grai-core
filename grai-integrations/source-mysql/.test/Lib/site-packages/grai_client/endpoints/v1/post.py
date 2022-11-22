from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1


@ClientV1.post.register
def post_node_v1(client: ClientV1, grai_type: NodeV1) -> NodeV1:
    url = client.node_endpoint
    response = client.post(url, grai_type.spec.dict())
    return NodeV1.from_spec(response.json())


@ClientV1.post.register
def post_edge_v1(client: ClientV1, grai_type: EdgeV1) -> EdgeV1:
    url = client.edge_endpoint

    source = grai_type.spec.source
    destination = grai_type.spec.destination
    if source.id is None:
        source = client.get(source)
    if destination.id is None:
        destination= client.get(destination)

    payload = grai_type.spec.dict()
    payload['source'] = source.id
    payload['destination'] = destination.id
    response = client.post(url, payload).json()
    if response is not None:
        response['source'] = source
        response['destination'] = destination
    return EdgeV1.from_spec(response)