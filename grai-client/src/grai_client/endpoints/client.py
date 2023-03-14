import abc
import sys
from typing import Any, Dict, List, Literal, Optional, Sequence, TypeVar, Union
from uuid import UUID

import requests
from multimethod import multimethod
from pydantic import BaseModel

from grai_client.authentication import APIKeyHeader, UserTokenHeader
from grai_client.endpoints.rest import delete, get, patch, post
from grai_client.endpoints.utilities import response_status_check, serialize_obj
from grai_client.schemas.schema import GraiType

if sys.version_info < (3, 10):
    from typing_extensions import ParamSpec
else:
    from typing import ParamSpec

P = ParamSpec("P")
R = TypeVar("R", covariant=True)
T = TypeVar("T")
OptionType = Optional[Union[Dict, "ClientOptions"]]
ResultTypes = Union[Optional[GraiType], Sequence[Optional[GraiType]]]


class ClientOptions(BaseModel):
    payload: Dict = {}
    request_args: Dict = {}
    headers: Dict = {}

    @classmethod
    def __hash__(cls):
        return id(cls)


PROTOCOL = Optional[Union[Literal["http"], Literal["https"]]]


class BaseClient(abc.ABC):
    id: str = "base"

    def __init__(self, host: str, port: str = "443", protocol: PROTOCOL = None, insecure: bool = False):
        self.host = host
        self.port = port
        self.insecure = insecure

        self.default_payload: Dict = dict()
        self.default_headers: Dict = dict()
        self.default_request_args: Dict = dict()
        self.session = requests.Session()

        if protocol is None:
            protocol = "http" if insecure else "https"
        self.protocol = protocol

        self.url = f"{self.protocol}://{self.host}:{self.port}"
        self.api = f"{self.url}"
        self.health_endpoint = f"{self.url}/health/"
        self._auth_headers: Optional[Dict[str, str]] = None

        resp = self.server_health_status()
        if resp.status_code != 200:
            raise Exception(f"Error connecting to server at {self.url}. Received response {resp.json()}")

    def default_options(self):
        return ClientOptions(
            **{
                "payload": self.default_payload,
                "headers": self.default_headers,
                "request_args": self.default_request_args,
            }
        )

    def server_health_status(self) -> requests.Response:
        return self.session.get(self.health_endpoint)

    def build_url(self, endpoint: str) -> str:
        return f"{self.api}{endpoint}"

    @property
    def auth_headers(self) -> Dict:
        if self._auth_headers is None:
            raise Exception(
                "Client not authenticated. Please call `set_authentication_headers` with your credentials first"
            )
        return self._auth_headers

    def set_authentication_headers(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        # Deprecated
        return self.authenticate(username, password, api_key)

    def authenticate(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        if api_key is not None:
            self._auth_headers = APIKeyHeader(api_key).headers
            self.session.auth = None
        elif username and password:
            self.session.auth = (username, password)
            self._auth_headers = {}
        else:
            raise Exception("Authentication requires either an api key, or username/password combination.")

        resp = self.check_authentication()
        if resp.status_code != 200:
            raise Exception(
                f"Unable to authenticate connection to the server with the provided credentials. Received status_code: {resp.status_code}"
            )

    @abc.abstractmethod
    def check_authentication(self) -> requests.Response:
        raise NotImplementedError(f"No authentication implemented for {type(self)}")

    @multimethod
    def get_url(self, grai_type: Any) -> str:
        raise NotImplementedError(f"No url method implemented for type {type(grai_type)}")

    def prep_options(self, options: OptionType = None) -> ClientOptions:
        default_options = self.default_options()
        if options is None:
            options = default_options
        if isinstance(options, ClientOptions):
            default_options.payload |= options.payload
            default_options.headers |= options.headers
            default_options.request_args |= options.request_args
        elif isinstance(options, Dict):
            default_options.payload |= options.get("payload", {})
            default_options.headers |= options.get("headers", {})
            default_options.request_args |= options.get("request_args", {})
        else:
            raise NotImplementedError(f"Unrecognized options type: {type(options)}")

        return default_options

    def get(self, *args, options: OptionType = None, **kwargs):
        options = self.prep_options(options)
        return get(self, *args, options=options, **kwargs)

    def post(self, *args, options: OptionType = None, **kwargs):
        options = self.prep_options(options)
        return post(self, *args, options=options, **kwargs)

    def patch(self, *args, options: OptionType = None, **kwargs):
        options = self.prep_options(options)
        return patch(self, *args, options=options, **kwargs)

    def delete(self, *args, options: OptionType = None, **kwargs):
        options = self.prep_options(options)
        return delete(self, *args, options=options, **kwargs)


@get.register
def get_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> Sequence[T]:
    result = [client.get(obj, options=options) for obj in objs]
    return result


@delete.register
def delete_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> None:
    for obj in objs:
        client.delete(obj, options=options)


@post.register
def post_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    result = [client.post(obj, options=options) for obj in objs]
    return result


@patch.register
def patch_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    result = [client.patch(obj, options=options) for obj in objs]
    return result


# -------------------------------------------- #


@get.register
def client_get_url(client: BaseClient, url: str, options: ClientOptions = ClientOptions()) -> requests.Response:
    headers = {**client.auth_headers, **options.headers}

    response = client.session.get(url, headers=headers, **options.request_args)
    response_status_check(response)
    return response


@delete.register
def client_delete_url(client: BaseClient, url: str, options: ClientOptions = ClientOptions()) -> requests.Response:
    headers = {**client.auth_headers, **options.headers}

    response = client.session.delete(url, headers=headers, **options.request_args)
    response_status_check(response)
    return response


@post.register
def client_post_url(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> requests.Response:
    headers = client.auth_headers
    headers = {
        **client.auth_headers,
        "Content-Type": "application/json",
        **options.headers,
    }
    payload = {**payload, **options.payload}

    response = client.session.post(url, data=serialize_obj(payload), headers=headers)  # , **options.request_args

    response_status_check(response)
    return response


@patch.register
def client_patch_url(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> requests.Response:
    headers = {
        **client.auth_headers,
        "Content-Type": "application/json",
        **options.headers,
    }
    payload = {**payload, **options.payload}

    response = client.session.patch(url, data=serialize_obj(payload), headers=headers, **options.request_args)

    response_status_check(response)
    return response
