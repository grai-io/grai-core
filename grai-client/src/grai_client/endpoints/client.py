import abc
import asyncio
import sys
from typing import (
    Any,
    Callable,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    TypeVar,
    Union,
)

import httpx
import tqdm
from httpx import BasicAuth, Request, Response
from multimethod import multimethod
from pydantic import BaseModel
from tqdm.asyncio import tqdm_asyncio

from grai_client.authentication import APIKeyHeader
from grai_client.endpoints.rest import delete, get, patch, post
from grai_client.endpoints.utilities import (
    add_query_params,
    response_status_check,
    serialize_obj,
)
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

    def __init__(
        self,
        host: str,
        port: str = "443",
        protocol: PROTOCOL = None,
        insecure: bool = False,
        httpx_async_client_args: Optional[Dict[str, Any]] = None,
    ):
        self.host = host
        self.port = port
        self.insecure = insecure

        self.default_payload: Dict = dict()
        self.default_headers: Dict = dict()
        self.default_request_args: Dict = dict()
        self.session = None
        self.httpx_async_client_args = httpx_async_client_args

        if protocol is None:
            protocol = "http" if insecure else "https"
        self.protocol = protocol

        self.url = f"{self.protocol}://{self.host}:{self.port}"
        self.api = f"{self.url}"
        self.health_endpoint = f"{self.url}/health"
        self._auth_headers: Optional[Dict[str, str]] = None
        self.auth: Optional[BasicAuth] = None
        resp = self.server_health_status()
        if resp.status_code != 200:
            raise Exception(f"Error connecting to server at {self.url}. Received response {resp.json()}")

    def get_session(self) -> httpx.AsyncClient:
        client_args = {"timeout": None, "http2": True}
        # client_args['limits'] = httpx.Limits(max_keepalive_connections=None, max_connections=None)
        client_args |= self.httpx_async_client_args if self.httpx_async_client_args is not None else {}

        session = httpx.AsyncClient(**client_args)
        session.auth = self.auth
        return session

    def default_options(self):
        return ClientOptions(
            **{
                "payload": self.default_payload,
                "headers": self.default_headers,
                "request_args": self.default_request_args,
            }
        )

    def server_health_status(self) -> Response:
        return httpx.get(self.health_endpoint)

    def build_url(self, endpoint: str) -> str:
        return f"{self.api}{endpoint}"

    @property
    def auth_headers(self) -> Dict:
        if self._auth_headers is None:
            raise Exception("Client not authenticated. Please call `authenticate` with your credentials first")
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
            self.auth = None
        elif username and password:
            self.auth = BasicAuth(username, password)
            self._auth_headers = {}
        else:
            raise Exception("Authentication requires either an api key, or username/password combination.")

        resp = self.check_authentication()
        if resp.status_code != 200:
            message = (
                f"Unable to authenticate connection to the server with the provided credentials. ",
                f"Received status_code: {resp.status_code}",
            )

            raise Exception(message)

    @abc.abstractmethod
    def check_authentication(self) -> Response:
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

    async def session_manager(self, async_func: Callable, *args, options: OptionType = None, **kwargs):
        async with self.get_session() as session:
            self.session = session
            options = self.prep_options(options)
            result = await async_func(self, *args, options=options, **kwargs)
        self.session = None
        return result

    def get(self, *args, options: OptionType = None, **kwargs):
        return asyncio.run(self.session_manager(get, *args, options=options, **kwargs))

    def post(self, *args, options: OptionType = None, **kwargs):
        return asyncio.run(self.session_manager(post, *args, options=options, **kwargs))

    def patch(self, *args, options: OptionType = None, **kwargs):
        return asyncio.run(self.session_manager(patch, *args, options=options, **kwargs))

    def delete(self, *args, options: OptionType = None, **kwargs):
        return asyncio.run(self.session_manager(delete, *args, options=options, **kwargs))


@get.register
async def get_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> Sequence[T]:
    result = await tqdm_asyncio.gather(*[get(client, obj, options=options) for obj in objs])
    return result


@delete.register
async def delete_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> None:
    await tqdm_asyncio.gather(*[delete(client, obj, options=options) for obj in objs])


@post.register
async def post_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    # result = await tqdm_asyncio.gather(*[post(client, obj, options=options) for obj in objs])

    tasks = [asyncio.create_task(post(client, obj, options=options)) for obj in objs]
    for task in tqdm.tqdm(asyncio.as_completed(tasks)):
        await task

    result = [t.result() for t in tasks]

    return result


@patch.register
async def patch_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    result = await tqdm_asyncio.gather(*[patch(client, obj, options=options) for obj in objs])
    return result


# -------------------------------------------- #


@get.register
async def client_get_url(client: BaseClient, url: str, options: ClientOptions = ClientOptions()) -> Response:
    headers = {**client.auth_headers, **options.headers}

    if "workspace" in options.payload:
        url = add_query_params(url, {"workspace": options.payload["workspace"]})

    response = await client.session.get(url, headers=headers, **options.request_args)
    response_status_check(response)
    return response


@delete.register
async def client_delete_url(client: BaseClient, url: str, options: ClientOptions = ClientOptions()) -> Response:
    headers = {**client.auth_headers, **options.headers}

    response = await client.session.delete(url, headers=headers, **options.request_args)
    response_status_check(response)
    return response


@post.register
async def client_post_url(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> Response:
    headers = {
        **client.auth_headers,
        "Content-Type": "application/json",
        **options.headers,
    }
    payload = {**payload, **options.payload}
    response = await client.session.post(url, content=serialize_obj(payload), headers=headers, **options.request_args)

    response_status_check(response)
    return response


@patch.register
async def client_patch_url(
    client: BaseClient,
    url: str,
    payload: Dict,
    options: ClientOptions = ClientOptions(),
) -> Response:
    headers = {
        **client.auth_headers,
        "Content-Type": "application/json",
        **options.headers,
    }
    payload = {**payload, **options.payload}

    response = await client.session.patch(url, content=serialize_obj(payload), headers=headers, **options.request_args)

    response_status_check(response)
    return response
