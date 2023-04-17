from grai_schemas.v1.node import NodeIdTypes

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get
from grai_client.endpoints.v1.client import ClientV1


async def process_node_id(
    client: ClientV1, grai_type: NodeIdTypes, options: ClientOptions = ClientOptions()
) -> NodeIdTypes:
    """
    Process a NodeID object, either by returning if it has a known id, or by getting
    the id from the server.
    """
    if grai_type.id is not None:
        return grai_type

    server_node = await get(client, grai_type, options=options)
    if server_node is None:
        if grai_type.id is None:
            message = (
                f"Could not find node with namespace=`{grai_type.namespace} " f"and name=`{grai_type.name}` on server"
            )
        else:
            message = f"Could not find node with id=`{grai_type.id}`"
        raise ValueError(message)

    return server_node.spec
