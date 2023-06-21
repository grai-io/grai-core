from typing import Dict, List, Literal, Optional, TypeVar, Union
from uuid import UUID

from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.edge import EdgeNamedID, EdgeUuidID, SourcedEdgeSpec, SourcedEdgeV1
from grai_schemas.v1.metadata.metadata import (
    GraiMalformedEdgeMetadataV1,
    GraiMalformedNodeMetadataV1,
)
from grai_schemas.v1.node import NodeNamedID, NodeUuidID, SourcedNodeSpec, SourcedNodeV1
from grai_schemas.v1.organization import OrganisationSpec, OrganisationV1
from grai_schemas.v1.source import SourceSpec, SourceV1
from grai_schemas.v1.workspace import WorkspaceSpec, WorkspaceV1

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get
from grai_client.endpoints.utilities import (
    handles_bad_metadata,
    is_valid_uuid,
    paginated,
)
from grai_client.endpoints.v1.client import ClientV1
from grai_client.errors import (
    InvalidResponseError,
    NotSupportedError,
    ObjectNotFoundError,
)
from grai_client.schemas.labels import (
    EdgeLabels,
    NodeLabels,
    OrganisationLabels,
    SourceEdgeLabels,
    SourceLabels,
    SourceNodeLabels,
    WorkspaceLabels,
)

T = TypeVar("T", NodeV1, EdgeV1)
X = TypeVar("X")


@handles_bad_metadata(GraiMalformedNodeMetadataV1)
def node_builder(resp: Dict[str, X]) -> NodeV1:
    return NodeV1.from_spec(resp)


@handles_bad_metadata(GraiMalformedNodeMetadataV1)
def source_node_builder(resp: Dict[str, X]) -> SourcedNodeV1:
    return SourcedNodeV1.from_spec(resp)


@handles_bad_metadata(GraiMalformedEdgeMetadataV1)
def edge_builder(resp: Dict[str, X]) -> EdgeV1:
    return EdgeV1.from_spec(resp)


@handles_bad_metadata(GraiMalformedEdgeMetadataV1)
def source_edge_builder(resp: Dict[str, X]) -> SourcedEdgeV1:
    return SourcedEdgeV1.from_spec(resp)


# ----- Nodes ----- #


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
    resp = paginated(get)(client, url, options)
    return [node_builder(obj) for obj in resp]


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
    return node_builder(resp)


@get.register
def get_from_node_uuid_id(client: ClientV1, grai_type: NodeUuidID, options: ClientOptions = ClientOptions()) -> NodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return get(client, "Node", grai_type.id, options=options)


@get.register
def get_from_node_named_id(
    client: ClientV1, grai_type: NodeNamedID, options: ClientOptions = ClientOptions()
) -> NodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    options = options.copy()
    options.query_args = {
        **options.query_args,
        "name": grai_type.name,
        "namespace": grai_type.namespace,
    }

    result = get(client, "Node", options=options)

    if (num_results := len(result)) == 0:
        raise ObjectNotFoundError(
            f"No Node found matching name={grai_type.name}, namespace={grai_type.namespace} "
            f"under the workspace `{client.workspace}`."
        )
    elif num_results == 1:
        return result[0]
    else:
        raise InvalidResponseError(
            f"A node query for name={grai_type.name}, namespace={grai_type.namespace} in the "
            f"workspace={client.workspace} returned more than one result. "
            f"This is a defensive error which should not be triggered. If you encounter it "
            "please open an issue at www.github.com/grai-io/grai-core/issues"
        )


# ----- SourcedNode ----- #


@get.register
def get_source_node_by_label_v1(
    client: ClientV1, grai_type: SourceNodeLabels, options: ClientOptions = ClientOptions()
) -> List[SourcedNodeV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    resp = paginated(get)(client, url, options)
    return [source_node_builder(obj) for obj in resp]


@get.register
def get_source_node_by_source_node_v1(
    client: ClientV1, grai_type: SourcedNodeV1, options: ClientOptions = ClientOptions()
) -> Optional[SourcedNodeV1]:
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
def get_source_node_by_source_node_v1(
    client: ClientV1, grai_type: SourcedNodeSpec, options: ClientOptions = ClientOptions()
) -> SourcedNodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """

    source_id = (
        grai_type.data_source.id if grai_type.data_source.id is not None else get(client, grai_type.data_source).spec.id
    )
    if grai_type.id is not None:
        node_id = grai_type.id
    else:
        sub_url = client.get_url("Node")
        sub_options = options.copy()
        sub_options.query_args.update({"name": grai_type.name, "namespace": grai_type.namespace})
        node = get(client, sub_url, sub_options)
        node_id = node.spec.id

    url = f"{client.get_url(grai_type)}/{source_id}/{node_id}/"
    resp = get(client, url, options=options).json()
    return source_node_builder(resp)


# ----- Edges ----- #


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
    resp = paginated(get)(client, url, options)
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

    result = get(client, "Edge", options=options)

    if (num_results := len(result)) == 0:
        raise ObjectNotFoundError(
            f"No Edge found matching name={grai_type.name}, namespace={grai_type.namespace} "
            f"under the workspace `{client.workspace}`."
        )
    elif num_results == 1:
        return result[0]
    else:
        raise InvalidResponseError(
            f"A edge query for name={grai_type.name}, namespace={grai_type.namespace} in the "
            f"workspace={client.workspace} returned more than one result. "
            f"This is a defensive error which should not be triggered. If you encounter it "
            "please open an issue at www.github.com/grai-io/grai-core/issues"
        )


# ----- SourcedNode ----- #


@get.register
def get_source_edge_by_label_v1(
    client: ClientV1, grai_type: SourceEdgeLabels, options: ClientOptions = ClientOptions()
) -> List[SourcedEdgeV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    resp = paginated(get)(client, url, options)
    finalized_result = (finalize_edge(client, edge) for edge in resp)
    return [source_edge_builder(edge) for edge in finalized_result]


@get.register
def get_source_node_by_source_node_v1(
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
def get_source_node_by_source_node_v1(
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

    source_id = (
        grai_type.data_source.id if grai_type.data_source.id is not None else get(client, grai_type.data_source).spec.id
    )
    if grai_type.id is not None:
        node_id = grai_type.id
    else:
        sub_url = client.get_url("Node")
        sub_options = options.copy()
        sub_options.query_args.update({"name": grai_type.name, "namespace": grai_type.namespace})
        node = get(client, sub_url, sub_options)
        node_id = node.spec.id

    url = f"{client.get_url(grai_type)}/{source_id}/{node_id}/"
    resp = get(client, url, options=options).json()
    finalized_result = finalize_edge(client, resp)
    return source_edge_builder(finalized_result)


# ----- Organisation ------ #


@get.register
def get_organisation_v1(
    client: ClientV1,
    grai_type: Union[OrganisationV1, OrganisationSpec, OrganisationLabels],
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
    message = "The get organisation endpoint is not supported through the REST API."
    raise NotSupportedError(message)


# ----- Workspaces ------ #


@get.register
def get_all_workspaces(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    options: ClientOptions = ClientOptions(),
) -> Optional[List[WorkspaceV1]]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    resp = paginated(get)(client, client.get_url(grai_type), options)

    if len(resp) == 0:
        return None
    else:
        return [WorkspaceV1.from_spec(item) for item in resp]


@get.register
def get_workspace_by_uuid(
    client: ClientV1,
    grai_type: WorkspaceLabels,
    workspace_id: Union[UUID, str],
    options: ClientOptions = ClientOptions(),
) -> Optional[WorkspaceV1]:
    """

    Args:
        client:
        grai_type:
        workspace_id:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    if not is_valid_uuid(workspace_id):
        message = f"The provided workspace id {workspace_id} is not a valid uuid."
        raise ValueError(message)
    url = f"{url}{workspace_id}/"
    result = get(client, url, options=options)
    return WorkspaceV1.from_spec(result.json())


@get.register
def get_workspace_by_workspace_v1(
    client: ClientV1,
    grai_type: WorkspaceV1,
    options: ClientOptions = ClientOptions(),
) -> WorkspaceV1:
    """

    Args:
        client:
        grai_type:
        name:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return get(client, grai_type.spec, options=options)


@get.register
def get_workspace_by_spec(
    client: ClientV1,
    grai_type: WorkspaceSpec,
    options: ClientOptions = ClientOptions(),
) -> WorkspaceV1:
    """

    Args:
        client:
        grai_type:
        name:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.id is not None:
        return get(client, "Workspace", grai_type.id, options=options)

    options = options.copy()
    options.query_args["ref"] = grai_type.ref

    resp = get(client, "Workspace", options)

    if resp is None:
        message = f"No Workspace found matching ref={grai_type.ref} under the workspace `{client.workspace}`."
        raise ObjectNotFoundError(message)
    elif len(resp) == 1:
        return WorkspaceV1.from_spec(resp[0])
    else:
        raise Exception(
            f"We were unable to identify a unique workspace matching ref=`{grai_type.ref}` because more than one result"
            f" was returned. This looks like a bug in the client library. Please open an issue at "
            f"www.github.com/grai-io/grai-core/issues."
        )


# ----- SourcedNode ----- #


@get.register
def get_source_node_by_label_v1(
    client: ClientV1, grai_type: SourceNodeLabels, options: ClientOptions = ClientOptions()
) -> List[SourcedNodeV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    resp = paginated(get)(client, url, options)
    return [source_node_builder(obj) for obj in resp]


@get.register
def get_source_node_by_source_node_v1(
    client: ClientV1, grai_type: SourcedNodeV1, options: ClientOptions = ClientOptions()
) -> Optional[SourcedNodeV1]:
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
def get_source_node_by_source_node_v1(
    client: ClientV1, grai_type: SourcedNodeSpec, options: ClientOptions = ClientOptions()
) -> SourcedNodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """

    source_id = (
        grai_type.data_source.id if grai_type.data_source.id is not None else get(client, grai_type.data_source).spec.id
    )
    if grai_type.id is not None:
        node_id = grai_type.id
    else:
        sub_url = client.get_url("Node")
        sub_options = options.copy()
        sub_options.query_args.update({"name": grai_type.name, "namespace": grai_type.namespace})
        node = get(client, sub_url, sub_options)
        node_id = node.spec.id

    url = f"{client.get_url(grai_type)}/{source_id}/{node_id}/"
    resp = get(client, url, options=options).json()
    return source_node_builder(resp)


# ----- Sources ------ #


@get.register
def get_all_sources(
    client: ClientV1,
    grai_type: SourceLabels,
    options: ClientOptions = ClientOptions(),
) -> List[SourceV1]:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    resp = paginated(get)(client, client.get_url(grai_type), options)
    for item in resp:
        item["workspace"] = client.workspace
    return [SourceV1.from_spec(item) for item in resp]


@get.register
def get_source_by_id(
    client: ClientV1,
    grai_type: SourceLabels,
    source_id: Union[str, UUID],
    options: ClientOptions = ClientOptions(),
) -> SourceV1:
    """

    Args:
        client:
        grai_type:
        source_id:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = f"{client.get_url(grai_type)}{source_id}/"
    resp = get(client, url, options).json()
    resp["workspace"] = client.workspace
    return SourceV1.from_spec(resp)


@get.register
def get_source_from_source_v1(
    client: ClientV1,
    grai_type: SourceV1,
    options: ClientOptions = ClientOptions(),
) -> SourceV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return get(client, grai_type.spec, options=options)


@get.register
def get_source_from_spec(
    client: ClientV1,
    grai_type: SourceSpec,
    options: ClientOptions = ClientOptions(),
) -> SourceV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.id is not None:
        return get(client, "Source", grai_type.id, options)

    url = client.get_url(grai_type)
    options = options.copy()
    options.query_args["name"] = grai_type.name

    result = paginated(get)(client, url, options=options)

    if (num_results := len(result)) == 0:
        message = f"No Source found matching name={grai_type.name} under the workspace `{client.workspace}`."
        raise ObjectNotFoundError(message)
    elif num_results == 1:
        return SourceV1.from_spec(result[0])
    else:
        raise InvalidResponseError(
            f"We were unable to identify a unique source matching name=`{grai_type.name}` under the workspace"
            f"`{client.workspace} because more than one "
            f"result was returned. This looks like a bug in the client library. Please open an issue at "
            f"www.github.com/grai-io/grai-core/issues."
        )
