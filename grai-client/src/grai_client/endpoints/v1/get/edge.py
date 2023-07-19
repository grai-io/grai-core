from typing import Dict, List, Optional, Union
from uuid import UUID

from grai_schemas.v1 import EdgeV1, SourcedEdgeV1, SourceV1
from grai_schemas.v1.edge import EdgeNamedID, EdgeUuidID, SourcedEdgeSpec

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get, get_is_unique, paginated_get
from grai_client.endpoints.utilities import is_valid_uuid, paginated, validated_uuid
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.get.utils import (
    edge_builder,
    get_source_and_spec,
    source_edge_builder,
)
from grai_client.errors import (
    InvalidResponseError,
    NotSupportedError,
    ObjectNotFoundError,
)
from grai_client.schemas.labels import EdgeLabels, SourceEdgeLabels


def finalize_edge(client: ClientV1, resp: Dict, options: ClientOptions = ClientOptions()) -> Dict:
    """

    Args:
        client:
        resp:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    nodes = [
        get(client, "node", resp["source"]),
        get(client, "node", resp["destination"]),
    ]

    resp["source"] = nodes[0].spec
    resp["destination"] = nodes[1].spec
    return resp


@get.register
def get_edge_by_label_v1(
    client: ClientV1, grai_type: EdgeLabels, options: ClientOptions = ClientOptions()
) -> List[EdgeV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    resp = paginated_get(client, url, options)
    finalized_result = (finalize_edge(client, edge) for edge in resp)
    return [edge_builder(edge) for edge in finalized_result]


@get.register
def get_edge_by_uuid_str_id(
    client: ClientV1,
    grai_type: EdgeLabels,
    edge_uuid: Union[str, UUID],
    options: ClientOptions = ClientOptions(),
) -> EdgeV1:
    """

    Args:
        client:
        grai_type:
        edge_uuid:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if not is_valid_uuid(edge_uuid):
        raise ValueError(f"The provided node id {edge_uuid} is not a valid uuid.")

    url = f"{client.get_url(grai_type)}{edge_uuid}/"

    resp = get(client, url, options=options)
    finalized_edge = finalize_edge(client, resp.json(), options)
    return edge_builder(finalized_edge)


@get.register
def get_edge_v1(client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()) -> Optional[EdgeV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return get(client, grai_type.spec, options)


@get.register
def get_from_edge_uuid_id(
    client: ClientV1, grai_type: EdgeUuidID, options: ClientOptions = ClientOptions()
) -> Optional[EdgeV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return get(client, "Edge", grai_type.id, options=options)


@get.register
def get_from_edge_named_id(
    client: ClientV1, grai_type: EdgeNamedID, options: ClientOptions = ClientOptions()
) -> EdgeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """

    if grai_type.id is not None:
        return get(client, "Edge", grai_type.id, options=options)

    options = options.copy()
    options.query_args = {
        **options.query_args,
        "name": grai_type.name,
        "namespace": grai_type.namespace,
    }

    return get_is_unique(client, "Edge", options=options)


# ----- SourcedEdge ----- #


@get.register
def get_source_edge_by_label_v1(
    client: ClientV1, grai_type: SourceEdgeLabels, options: ClientOptions = ClientOptions()
):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    raise NotSupportedError("It's not possible to query for lineage sources without a source id.")


@get.register
def get_source_edge_by_label_and_id_v1(
    client: ClientV1, grai_type: SourceEdgeLabels, source_id: Union[str, UUID], options: ClientOptions = ClientOptions()
) -> List[SourcedEdgeV1]:
    """

    Args:
        client:
        grai_type:
        source_id:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if (source_id := validated_uuid(source_id)) is None:
        source: SourceV1 = get_is_unique(client, "Source", name=source_id)
        source_id = source.spec.id
    else:
        source = get(client, "Source", source_id)

    url = client.get_url(grai_type, source_id)
    resp = paginated_get(client, url, options)

    result = []
    for edge in resp:
        edge["data_source"] = source.spec
        edge = finalize_edge(client, edge)
        result.append(source_edge_builder(edge))
    return result


@get.register
def get_source_edge_by_source_edge_v1(
    client: ClientV1, grai_type: SourcedEdgeV1, options: ClientOptions = ClientOptions()
) -> SourcedEdgeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return get(client, grai_type.spec, options)


@get.register
def get_source_edge_by_source_edge_spec(
    client: ClientV1, grai_type: SourcedEdgeSpec, options: ClientOptions = ClientOptions()
) -> SourcedEdgeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """

    source, edge = get_source_and_spec(client, grai_type)

    url = client.get_url("SourceEdge", source.id, edge.id)
    resp = get(client, url, options=options).json()
    finalized_result = finalize_edge(client, resp)
    return source_edge_builder(finalized_result)
