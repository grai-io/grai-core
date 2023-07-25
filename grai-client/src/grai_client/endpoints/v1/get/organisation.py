from typing import Union

from grai_schemas.v1 import OrganisationV1
from grai_schemas.v1.organization import OrganisationSpec

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get
from grai_client.endpoints.v1.client import ClientV1
from grai_client.errors import NotSupportedError
from grai_client.schemas.labels import OrganisationLabels


@get.register
def get_organisation_v1(
    client: ClientV1,
    grai_type: OrganisationLabels,
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


@get.register
def get_organisation_v1(
    client: ClientV1,
    grai_type: Union[OrganisationV1, OrganisationSpec],
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
