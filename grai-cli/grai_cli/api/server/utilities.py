import json
from typing import Dict
from grai_cli import config
import requests
import typer


class GraiServerConfig:
    json_headers = {
            "accept": "application/json",
            "Content-Type": "application/json"
        }

    def __init__(self):
        server_configs = config.get({
            'server': {
                "host": str,
                "port": str,
            }
        })
        self.host = server_configs['server']['host']
        self.port = server_configs['server']['port']
        self.url = f"http://{self.host}:{self.port}"
        self.api = f"{self.url}"
        self.headers = {}

    def authenticate_with_username(self):
        params = {
            'auth': {
                "username": str,
                "password": str,
            }
        }
        raise Exception("not implemented")
        params = config.get(params)

    def authenticate_with_token(self):
        params = {
            'auth': {"token": str}
        }
        token = config.get(params)
        header = {"Authorization": f"Token {token}"}
        self.headers.update(header)
        return header

    def authenticate_with_api_key(self):
        api_key = config.grab('auth.api_key')
        header = {"Authorization": f"Api-Key {api_key}"}
        self.headers.update(header)
        return header

    def get_jwt(self, username, password):
        response = requests.post(f"{self.api}/token/", headers=self.json_headers, params=self.user_auth_params)
        if response.status_code != 200:
            raise

        return response.json()

    def authenticate(self):
        modes = {
            'username': self.authenticate_with_username,
            'api': self.authenticate_with_api_key
        }
        auth_mode = config.grab('auth.authentication_mode')
        return modes[auth_mode]()


def response_auth_checker(fn):
    def response_status_check(response):
        if response.status_code in {200, 201}:
            pass
        elif response.status_code in {400, 401, 402, 403}:
            typer.echo(f"Failed to Authenticate with code: {response.status_code}")
        elif response.status_code == 404:
            typer.echo(f"No server endpoint found for this request")
        else:
            raise NotImplementedError(f"No handling for error code {response.status_code}")
        return response

    def inner(*args, **kwargs):
        response = fn(*args, **kwargs)
        response_status_check(response)
        return response.json()

    return inner


class EndpointBuilder:
    def __init__(self, endpoint, headers):
        self.endpoint = endpoint
        self.headers = headers

    @response_auth_checker
    def get(self):
        response = requests.get(self.endpoint, headers=self.headers)
        return response

    @response_auth_checker
    def post(self, data):
        response = requests.post(self.endpoint, data=json.dumps(data), headers=self.headers)
        return response


class GraiV1Endpoints(GraiServerConfig):
    base = '/api/v1'
    _is_authenticated = '/auth/is-authenticated/'
    _node_endpoint = '/lineage/nodes/'
    _nodes = False

    def build_url(self, endpoint):
        return f"{self.api}{self.base}{endpoint}"

    def check_authentication(self):
        url = self.build_url(self._is_authenticated)
        self.authenticate()
        result = requests.get(url, headers=self.headers | self.json_headers)
        return result

    def nodes(self) -> EndpointBuilder:
        if self._nodes is False:
            url = self.build_url(self._node_endpoint)
            self.authenticate()
            self._nodes = EndpointBuilder(url, headers=self.headers | self.json_headers)
        return self._nodes


def get_endpoints(spec: Dict | None = None, version: str = "default") -> GraiServerConfig:
    mappings = {
        'v1': GraiV1Endpoints(),
    }
    mappings['default'] = mappings['v1']

    if spec is None:
        return mappings[version]

    if spec['version'] not in mappings:
        raise NotImplementedError(f"No endpoints defined for version {spec['version']}")
    return mappings[spec['version']]


def get_endpoint_from_spec(spec: Dict):
    mapper = {
        'Node': 'nodes'
    }
    endpoints = get_endpoints(spec)
    return getattr(endpoints, mapper[spec['type']])

