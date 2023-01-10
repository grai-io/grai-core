from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.node import NodeID


def process_node_id(
    client: ClientV1, grai_type: NodeID, options: ClientOptions = ClientOptions()
) -> NodeID:
    """
    Process a NodeID object, either by returning if it has a known id, or by getting
    the id from the server.
    """
    if grai_type.id is not None:
        return grai_type

    server_node = client.get(grai_type, options=options)
    if server_node is None:
        message = (
            f"Could not find node with namespace=`{grai_type.namespace} "
            f"and name=`{grai_type.name}` on server"
        )
        raise ValueError(message)

    return server_node
