from typing import TypeVar

from grai_client.endpoints.v1.client import ClientV1
from grai_client.schemas import edge, node
from grai_client.schemas.utilities import merge_models

T = TypeVar("T", node.NodeV1, edge.EdgeV1)


@ClientV1.patch.register
def patch_obj_v1(client: ClientV1, grai_type: node.NodeV1) -> node.NodeV1:
    if grai_type.spec.id is None:
        current = client.get(grai_type)
        grai_type.spec.id = current.spec.id

    base_url = client.get_url(grai_type)
    url = f"{base_url}{grai_type.spec.id}/"
    response = client.patch(url, grai_type.spec.json(exclude_none=True, models_as_dict=True)).json()
    if response is None:
        return None
    return node.NodeV1.from_spec(response)


@ClientV1.patch.register
def patch_obj_v1(client: ClientV1, grai_type: edge.EdgeV1) -> edge.EdgeV1:
    if grai_type.spec.id is None:
        current = client.get(grai_type)
        grai_type.spec.id = current.spec.id

    base_url = client.get_url(grai_type)
    url = f"{base_url}{grai_type.spec.id}/"

    source = grai_type.spec.source
    destination = grai_type.spec.destination
    if source.id is None:
        source = client.get(source)
        grai_type.spec.source.id = source.id
    if destination.id is None:
        destination = client.get(destination)
        grai_type.spec.destination.id = destination.id

    print(grai_type.spec.json(exclude_none=True, models_as_dict=True))
    response = client.patch(url, grai_type.spec.json(exclude_none=True, models_as_dict=True)).json()
    if response is not None:
        response["source"] = source
        response["destination"] = destination

    return edge.EdgeV1.from_spec(response)
