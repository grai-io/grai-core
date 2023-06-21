from typing import Dict, List, Optional, Union
from uuid import UUID

from grai_schemas.v1 import EdgeV1, NodeV1, WorkspaceV1
from grai_schemas.v1.edge import EdgeSpec, SourcedEdgeV1
from grai_schemas.v1.node import NodeSpec, SourcedNodeV1
from grai_schemas.v1.organization import OrganisationSpec, OrganisationV1
from grai_schemas.v1.source import SourceSpec, SourceV1

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get, post
from grai_client.endpoints.v1.client import ClientV1
from grai_client.endpoints.v1.utils import process_node_id
from grai_client.errors import NotSupportedError


def collect_data_sources(data_sources: List[Union[UUID, SourceSpec]]) -> List[Union[Dict, SourceSpec]]:
    """

    Args:
        data_sources:

    Returns:

    Raises:

    """
    data_sources = []
    for source in data_sources:
        if isinstance(source, UUID):
            source_obj = {"id": source}
        elif isinstance(source, SourceSpec):
            source_obj = source
        else:
            raise NotSupportedError(f"Only UUIDs and SourceSpecs are supported not {type(source)}")

        data_sources.append(source_obj)

    return data_sources


@post.register
def post_node_by_spec(client: ClientV1, grai_type: NodeSpec, options: ClientOptions = ClientOptions()) -> NodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)
    payload = grai_type.dict(exclude_none=True)
    payload["data_sources"] = collect_data_sources(grai_type.data_sources)

    response = post(client, url, payload, options=options)
    return NodeV1.from_spec(response.json())


@post.register
def post_node_by_spec(client: ClientV1, grai_type: NodeV1, options: ClientOptions = ClientOptions()) -> NodeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return post(client, grai_type.spec, options)


@post.register
def post_sourced_node_v1(
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
    url = client.get_url(grai_type)
    response = post(client, url, grai_type.spec.dict(exclude_none=True), options=options)
    return SourcedNodeV1.from_spec(response.json())


@post.register
def post_edge_by_spec(client: ClientV1, grai_type: EdgeSpec, options: ClientOptions = ClientOptions()) -> EdgeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    url = client.get_url(grai_type)

    payload = grai_type.dict(exclude_none=True)
    payload["data_sources"] = collect_data_sources(grai_type.data_sources)

    response = post(client, url, payload, options=options)
    response = response.json()

    response["source"] = {**payload["source"], "id": response["source"]}
    response["destination"] = {**payload["destination"], "id": response["destination"]}

    return EdgeV1.from_spec(response)


@post.register
def post_edge_by_edge_v1(client: ClientV1, grai_type: EdgeV1, options: ClientOptions = ClientOptions()) -> EdgeV1:
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    return post(client, grai_type.spec, options)


@post.register
def post_workspace_v1(
    client: ClientV1, grai_type: WorkspaceV1, options: ClientOptions = ClientOptions()
) -> WorkspaceV1:
    """
    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:
    """
    url = client.get_url(grai_type)
    payload = grai_type.spec.dict(exclude_none=True)

    if isinstance(grai_type.spec.organisation, UUID):
        organisation_id = grai_type.spec.organisation
    elif isinstance(grai_type.spec.organisation, OrganisationSpec) and grai_type.spec.organisation.id is not None:
        organisation_id = grai_type.spec.organisation.id
    else:
        error_message = (
            f"An attempt was made to post the workspace `{grai_type.spec.ref}`. Unfortunately, no Organisation id was"
            f"provided as part of the request and the client library does not currently support posting a workspace "
            f"without an organisation id."
        )
        raise ValueError(error_message)

    payload["organisation"] = organisation_id

    response = post(client, url, payload, options=options)
    return WorkspaceV1.from_spec(response.json())


@post.register
def post_source_v1(client: ClientV1, grai_type: SourceSpec, options: ClientOptions = ClientOptions()) -> SourceV1:
    """
    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:
    """
    url = client.get_url(grai_type)

    if grai_type.workspace_id is not None:
        if client.workspace != str(grai_type.workspace_id):
            message = (
                f"The workspace id provided in the source {grai_type} does not match the client's "
                f"workspace id {client.workspace}."
            )
            raise ValueError(message)

    payload = grai_type.dict(exclude_none=True)
    response = post(client, url, payload, options=options).json()
    response["workspace"] = client.workspace
    return SourceV1.from_spec(response)


@post.register
def post_source_v1(client: ClientV1, grai_type: SourceV1, options: ClientOptions = ClientOptions()) -> SourceV1:
    """
    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:
    """
    return post(client, grai_type.spec, options)


@post.register
def post_organisation_v1(
    client: ClientV1, grai_type: Union[OrganisationV1, OrganisationSpec], options: ClientOptions = ClientOptions()
):
    """

    Args:
        client:
        grai_type:
        options:  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    message = "The post organisation endpoint is not supported through the REST API."
    raise NotSupportedError(message)
