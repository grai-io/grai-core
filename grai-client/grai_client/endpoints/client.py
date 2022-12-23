import abc
import sys
from typing import Any, Dict, List, Optional, Sequence, TypeVar, Union

import requests
from grai_client.authentication import APIKeyHeader, UserNameHeader, UserTokenHeader
from grai_client.endpoints.rest import delete, get, patch, post
from grai_client.endpoints.utilities import response_status_check, serialize_obj
from grai_client.schemas.schema import GraiType
from multimethod import multimethod
from pydantic import BaseModel

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


class BaseClient(abc.ABC):
    id = "base"

    def __init__(self, host: str, port: str, workspace: Optional[str] = None):
        self.host = host
        self.port = port
        self.workspace = workspace

        self.default_payload = {} if workspace is None else {"workspace": workspace}
        self.default_headers = {}
        self.default_request_args = {}
        self.default_options = ClientOptions(
            **{
                "payload": self.default_payload,
                "headers": self.default_headers,
                "request_args": self.default_request_args,
            }
        )

        prefix = "https" if self.port == "443" else "http"
        self.url = f"{prefix}://{self.host}:{self.port}"
        self.api = f"{self.url}"
        self._auth_headers: Optional[Dict[str, str]] = None

        if not self.check_server_status():
            raise Exception(f"Server at {self.url} is not responding.")

    def check_server_status(self) -> bool:
        resp = requests.get(f"{self.url}/health/")
        return resp.status_code == 200

    def build_url(self, endpoint: str) -> str:
        return f"{self.api}{endpoint}"

    @property
    def auth_headers(self) -> Dict:
        if not self._auth_headers:
            raise Exception(
                "Client not authenticated. Please call `set_authentication_headers` with your credentials first"
            )
        return self._auth_headers

    def set_authentication_headers(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        token: Optional[str] = None,
        api_key: Optional[str] = None,
    ) -> None:
        if username and password:
            self._auth_headers = UserNameHeader(username, password, self.url).headers
        elif token:
            self._auth_headers = UserTokenHeader(token).headers
        elif api_key:
            self._auth_headers = APIKeyHeader(api_key).headers
        else:
            raise Exception(
                "Authentication requires either a user token, api key, or username/password combination."
            )

    def check_authentication(self) -> requests.Response:
        raise NotImplementedError(f"No authentication implemented for {type(self)}")

    @multimethod
    def get_url(self, grai_type: Any) -> str:
        raise NotImplementedError(
            f"No url method implemented for type {type(grai_type)}"
        )

    def prep_options(self, options: OptionType = None) -> ClientOptions:
        if options is None:
            options = self.default_options
        if isinstance(options, ClientOptions):
            options = ClientOptions(**{**self.default_options.dict(), **options.dict()})
        elif isinstance(options, Dict):
            options = ClientOptions(**{**self.default_options.dict(), **options})
        else:
            raise NotImplementedError(f"Unrecognized options type: {type(options)}")

        return options

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
    objs: Sequence[Union[str, T]],
    options: ClientOptions = ClientOptions(),
) -> Sequence[T]:
    result = [client.get(obj, options=options) for obj in objs]
    return result


@delete.register
def delete_sequence(
    client: BaseClient,
    objs: Sequence[Union[str, T]],
    options: ClientOptions = ClientOptions(),
) -> None:
    for obj in objs:
        client.delete(obj, options=options)


@post.register
def post_sequence(
    client: BaseClient,
    objs: Sequence[Union[str, T]],
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    result = [client.post(obj, options=options) for obj in objs]
    return result


@patch.register
def patch_sequence(
    client: BaseClient,
    objs: Sequence[Union[str, T]],
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    result = [client.patch(obj, options=options) for obj in objs]
    return result


# -------------------------------------------- #


@get.register
def get_url(
    client: BaseClient, url: str, options: ClientOptions = ClientOptions()
) -> requests.Response:
    headers = {**client.auth_headers, **options.headers}

    response = requests.get(url, headers=headers, **options.request_args)
    response_status_check(response)
    return response


@delete.register
def delete_url(
    client: BaseClient, url: str, options: ClientOptions = ClientOptions()
) -> requests.Response:
    headers = {**client.auth_headers, **options.headers}

    response = requests.delete(url, headers=headers, **options.request_args)
    response_status_check(response)
    return response


@post.register
def post_url(
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

    response = requests.post(
        url, data=serialize_obj(payload), headers=headers  # , **options.request_args
    )

    response_status_check(response)
    return response


@patch.register
def patch_url(
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

    response = requests.patch(
        url, data=serialize_obj(payload), headers=headers, **options.request_args
    )

    response_status_check(response)
    return response
