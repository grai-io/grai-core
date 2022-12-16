from typing import TypeVar
from grai_client.endpoints.v1.utils import process_node_id
from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas import edge, node
from grai_client.schemas.utilities import merge_models

T = TypeVar("T", node.NodeV1, edge.EdgeV1)



@ClientV1.patch.register
def patch_obj_v1(client: ClientV1, grai_type: node.NodeV1) -> node.NodeV1:
    if grai_type.spec.id is None:
        current = client.get(grai_type)
        grai_type.spec.id = current.spec.id

    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"
    response = client.patch(url, grai_type.spec.dict(exclude_none=True)).json()
    if response is None:
        return None
    return node.NodeV1.from_spec(response)


@ClientV1.patch.register
def patch_obj_v1(client: ClientV1, grai_type: edge.EdgeV1) -> edge.EdgeV1:
    if grai_type.spec.id is None:
        current = client.get(grai_type)
        grai_type.spec.id = current.spec.id

    url = f"{client.get_url(grai_type)}{grai_type.spec.id}/"

    source = process_node_id(client, grai_type.spec.source)
    destination = process_node_id(client, grai_type.spec.destination)

    payload = grai_type.spec.dict(exclude_none=True)
    payload["source"] = source.id
    payload["destination"] = destination.id

    response = client.patch(url, payload).json()
    if response is None:
        return None

    response["source"] = source
    response["destination"] = destination
    return edge.EdgeV1.from_spec(response)
