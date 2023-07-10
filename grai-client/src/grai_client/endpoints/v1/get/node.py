from typing import List, Union
from uuid import UUID

from grai_schemas.v1 import NodeV1, SourcedNodeV1, SourceV1
from grai_schemas.v1.node import NodeSpec, SourcedNodeSpec
from grai_schemas.v1.source import SourceSpec

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get, get_is_unique, paginated_get
from grai_client.endpoints.utilities import is_valid_uuid, validated_uuid
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.get.utils import (
    get_source_and_spec,
    node_builder,
    source_node_builder,
)
from grai_client.errors import NotSupportedError
from grai_client.schemas.labels import NodeLabels, SourceNodeLabels


@get.register
def get_node_by_label_v1(
    client: ClientV1, grai_type: NodeLabels, options: ClientOptions = ClientOptions()
) -> List[NodeV1]:
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
    return [node_builder(obj) for obj in resp]


@get.register
def get_nodes_by_uuid_str_id(
    client: ClientV1,
    grai_type: NodeLabels,
    node_uuid: Union[str, UUID],
    options: ClientOptions = ClientOptions(),
) -> NodeV1:
    """

    Args:
        client:
        grai_type:
        node_uuid:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if not is_valid_uuid(node_uuid):
        raise ValueError(f"The provided node id {node_uuid} is not a valid uuid.")

    url = f"{client.get_url(grai_type)}{node_uuid}/"

    resp = get(client, url, options=options)
    resp = resp.json()
    for data_source in resp["data_sources"]:
        data_source["workspace"] = client.workspace
    return node_builder(resp)


@get.register
def get_node_v1(client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()) -> NodeV1:
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
def get_from_node_spec(client: ClientV1, grai_type: NodeSpec, options: ClientOptions = ClientOptions()) -> NodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.id is not None:
        return get(client, "Node", grai_type.id, options=options)

    options = options.copy()
    options.query_args = {
        **options.query_args,
        "name": grai_type.name,
        "namespace": grai_type.namespace,
    }

    return get_is_unique(client, "Node", options=options)


# ----- SourcedNode ----- #


@get.register
def get_source_node_by_label_v1(
    client: ClientV1,
    grai_type: SourceNodeLabels,
    options: ClientOptions = ClientOptions(),
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
def get_source_node_by_label_and_id_v1(
    client: ClientV1,
    grai_type: SourceNodeLabels,
    source_id: Union[str, UUID],
    options: ClientOptions = ClientOptions(),
) -> List[SourcedNodeV1]:
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
        source = get(client, "Source", source_id, options=options)

    url = client.get_url(grai_type, source_id)
    resp = paginated_get(client, url, options)

    for item in resp:
        item["data_source"] = source.spec
    return [source_node_builder(obj) for obj in resp]


@get.register
def get_source_node_by_source_node_v1(
    client: ClientV1, grai_type: SourcedNodeV1, options: ClientOptions = ClientOptions()
) -> SourcedNodeV1:
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
def get_source_node_by_source_node_spec(
    client: ClientV1,
    grai_type: SourcedNodeSpec,
    options: ClientOptions = ClientOptions(),
) -> SourcedNodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    source, node = get_source_and_spec(client, grai_type)

    url = client.get_url("SourceNode", source.id, node.id)
    resp = get(client, url, options=options).json()
    resp["data_source"]: SourceSpec = source

    return source_node_builder(resp)
