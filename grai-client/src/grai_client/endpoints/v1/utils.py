from uuid import uuid4

from grai_schemas.v1.node import NodeIdTypes

from grai_client.endpoints.client import ClientOptions
from grai_client.endpoints.rest import get
from grai_client.endpoints.v1.client import ClientV1


def process_node_id(client: ClientV1, grai_type: NodeIdTypes, options: ClientOptions = ClientOptions()) -> NodeIdTypes:
    """Process a NodeID object, either by returning if it has a known id, or by getting
    the id from the server.

    Args:
        client (ClientV1):
        grai_type (NodeIdTypes):
        options (ClientOptions, optional):  (Default value = ClientOptions())

    Returns:

    Raises:

    """
    if grai_type.id is not None:
        return grai_type

    server_node = get(client, grai_type, options=options)
    if server_node is None:
        if grai_type.id is None:
            message = (
                f"Could not find node with namespace=`{grai_type.namespace} " f"and name=`{grai_type.name}` on server"
            )
        else:
            message = f"Could not find node with id=`{grai_type.id}`"
        raise ValueError(message)

    return server_node.spec


class MockClientV1(ClientV1):
    """A mock client that can be used for testing."""

    def __init__(self, workspace=None, **kwargs):
        self._workspace = str(uuid4()) if workspace is None else workspace
        username = kwargs.get("username", "null@grai.io")
        password = kwargs.get("password", "super_secret")
        url = kwargs.get("url", "http://localhost:8000")
        super().__init__(workspace=workspace, username=username, password=password, url=url, **kwargs)

    @property
    def workspace(self):
        return self._workspace

    def authenticate(*args, **kwargs) -> None:
        pass
