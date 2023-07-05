from typing import List, Union
from uuid import UUID

from grai_schemas.v1 import SourceV1
from grai_schemas.v1.source import SourceSpec

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get, paginated_get
from grai_client.endpoints.utilities import expects_unique_query, paginated
from grai_client.endpoints.v1.client import ClientV1
from grai_client.errors import InvalidResponseError, ObjectNotFoundError
from grai_client.schemas.labels import SourceLabels


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
    resp = paginated_get(client, client.get_url(grai_type), options)
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

    validated_query = expects_unique_query(paginated_get)
    result = validated_query(client, url, options=options)
    return SourceV1.from_spec(result)
