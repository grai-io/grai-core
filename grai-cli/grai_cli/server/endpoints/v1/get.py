from grai_cli.settings.schemas.edge import EdgeV1, EdgeType, EdgeNodeValues
from grai_cli.settings.schemas.node import NodeV1, NodeType
from grai_cli.server.endpoints.v1.client import ClientV1
from grai_cli.server.utilities import response_auth_checker
import requests


@ClientV1.get.register(str)
@response_auth_checker
def _(client: ClientV1, url: str) -> requests.request:
    headers = client.authentication_headers()
    response = requests.get(url, headers=headers)
    return response


@ClientV1.get.register(NodeV1)
@ClientV1.get.register(NodeType)
def _(client: ClientV1, grai_type: NodeV1) -> requests.request:
    url = client.node_endpoint
    return client.get(url)


def url_with_filters(self, **kwargs) -> str:
    filters = '&'.join([f"{k}={v}" for k, v in kwargs.items()])
    return f'{self.endpoint}?{filters}'


@ClientV1.get.register(EdgeNodeValues)
def _(client: ClientV1, node_values: EdgeNodeValues) -> requests.request:
    url = f'{client.node_endpoint}?name={node_values.name}&namespace={node_values.namespace}'
    return client.get(url)


@ClientV1.get.register(EdgeV1)
@ClientV1.get.register(EdgeType)
def _(client: ClientV1, grai_type: EdgeV1) -> requests.request:
    url = client.edge_endpoint
    return client.get(url)




