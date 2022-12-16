from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeID, NodeV1


@ClientV1.post.register
def post_node_v1(client: ClientV1, grai_type: NodeV1) -> NodeV1:
    url = client.node_endpoint
    response = client.post(url, grai_type.spec.dict())
    return NodeV1.from_spec(response.json())


def process_node_id(client: ClientV1, grai_type: NodeID) -> NodeID:
    """
    Process a NodeID object, either by returning if it has a known id, or by getting
    the id from the server.
    """
    if grai_type.id is not None:
        return grai_type

    server_node = client.get(grai_type)
    if server_node is None:
        message = (
            f"Could not find node with namespace=`{grai_type.namespace} "
            f"and name=`{grai_type.name}` on server"
        )
        raise ValueError(message)

    return server_node


@ClientV1.post.register
def post_edge_v1(client: ClientV1, grai_type: EdgeV1) -> EdgeV1:
    url = client.edge_endpoint

    source = process_node_id(client, grai_type.spec.source)
    destination = process_node_id(client, grai_type.spec.destination)

    payload = grai_type.spec.dict()
    payload["source"] = source.id
    payload["destination"] = destination.id
    response = client.post(url, payload).json()

    if response is not None:
        response["source"] = source
        response["destination"] = destination
    return EdgeV1.from_spec(response)
