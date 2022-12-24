from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import delete
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas.edge import EdgeV1
from grai_client.schemas.node import NodeV1


@delete.register
def delete_node_v1(
    client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()
):
    if grai_type.spec.id is None:
        grai_type = client.get(grai_type)
        if grai_type is None:
            return
    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    client.delete(url, options=options)


@delete.register
def delete_edge_v1(
    client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()
):
    if grai_type.spec.id is None:
        grai_type = client.get(grai_type)
        if grai_type is None:
            return
    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    client.delete(url, options=options)
