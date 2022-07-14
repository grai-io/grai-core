import json
from typing import Dict, Type
from grai_cli import config
import requests
import typer
from grai_cli.settings.schemas.schema import GraiType
from grai_cli.settings.schemas.edge import EdgeNodeValues



def response_auth_checker(fn):
    def response_status_check(response):
        if response.status_code in {200, 201}:
            return response
        elif response.status_code in {400, 401, 402, 403}:
            typer.echo(f"Failed to Authenticate with code: {response.status_code}")
            raise typer.Exit()
        elif response.status_code == 404:
            typer.echo(response.reason)
            raise typer.Exit()
        elif response.status_code == 500:
            typer.echo(response.text)
            message = ("Hit an internal service error, this looks like a bug, sorry! "
                       "Please submit a bug report to https://github.com/grai-io/grai-core/issues")
            typer.echo(message)
            raise typer.Exit()
        else:
            typer.echo(f"No handling for error code {response.status_code}")
            raise typer.Exit()

    def inner(*args, **kwargs):
        response = fn(*args, **kwargs)
        response = response_status_check(response)
        return response.json()

    return inner


class EndpointBuilder:
    def __init__(self, endpoints, endpoint, headers):
        self.endpoints = endpoints
        self.endpoint = endpoint
        self.headers = headers

    @response_auth_checker
    def get(self, url=None):
        if url is None:
            url = self.endpoint
        response = requests.get(url, headers=self.headers)
        return response

    @response_auth_checker
    def post(self, data):
        response = requests.post(self.endpoint, data=json.dumps(data.dict()), headers=self.headers)
        return response

    def url_with_filters(self, **kwargs):
        filters = '&'.join([f"{k}={v}" for k, v in kwargs.items()])
        return f'{self.endpoint}?{filters}'


class EdgeEndpointBuilder(EndpointBuilder):
    @response_auth_checker
    def post(self, data: Type[GraiType]):
        values = data.spec
        if isinstance(values.source, EdgeNodeValues):
            url = self.endpoints.nodes.url_with_filters(values.source.dict())
            values.source = self.endpoints.nodes.get(url).json()['id']
        if isinstance(values.destination, EdgeNodeValues):
            url = self.endpoints.nodes.url_with_filters(values.destination.dict())
            values.destination = self.endpoints.nodes.get(url).json()['id']
        super().post(values.dict())


# class GraiV1Endpoints(GraiServerConfig):
#     base = '/api/v1'
#     _is_authenticated = '/auth/is-authenticated/'
#     _node_endpoint = '/lineage/nodes/'
#     _nodes = False
#     _edge_endpoint = '/lineage/edges/'
#     _edges = False
#
#     def build_url(self, endpoint):
#         return f"{self.api}{self.base}{endpoint}"
#
#     def check_authentication(self):
#         url = self.build_url(self._is_authenticated)
#         self.authenticate()
#         result = requests.get(url, headers=self.headers | self.json_headers)
#         return result
#
#     def nodes(self) -> EndpointBuilder:
#         if self._nodes is False:
#             url = self.build_url(self._node_endpoint)
#             self.authenticate()
#             self._nodes = EndpointBuilder(self, url, headers=self.headers | self.json_headers)
#         return self._nodes
#
#     def edges(self) -> EndpointBuilder:
#         if self._edges is False:
#             url = self.build_url(self._edge_endpoint)
#             self.authenticate()
#             self._edges = EdgeEndpointBuilder(self, url, headers=self.headers | self.json_headers)
#         return self._edges


_endpoint_versions = {
    'v1': GraiV1Endpoints(),
    'default': GraiV1Endpoints(),
}


def get_endpoints(spec: Type[GraiType] | None) -> GraiServerConfig:
    if spec is None:
        return _endpoint_versions['default']

    if spec.version not in _endpoint_versions:
        raise NotImplementedError(f"No endpoints defined for version {spec['version']}")
    return _endpoint_versions[spec.version]


def get_endpoint_from_spec(spec: Type[GraiType]):
    mapper = {
        'Node': 'nodes',
        'Edge': 'edges'
    }
    endpoints = get_endpoints(spec)
    return getattr(endpoints, mapper[spec.type])

