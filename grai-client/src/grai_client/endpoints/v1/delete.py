from grai_schemas.v1 import EdgeV1, NodeV1

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import delete, get
from grai_client.endpoints.v1.client import ClientV1


@delete.register
async def delete_node_v1(client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()):
    if grai_type.spec.id is None:
        grai_type = await get(client, grai_type)
        if grai_type is None:
            return
    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    await delete(client, url, options=options)


@delete.register
async def delete_edge_v1(client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()):
    if grai_type.spec.id is None:
        grai_type = await get(client, grai_type)
        if grai_type is None:
            return
    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    await delete(client, url, options=options)
