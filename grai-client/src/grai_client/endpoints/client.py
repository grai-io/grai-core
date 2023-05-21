import abc
import asyncio
import json
import sys
import warnings
from functools import wraps
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    TypeVar,
    Union,
)
from urllib.parse import urlparse

import httpx
import tqdm
from grai_schemas.base import Edge, Node
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
OptionType = Union[Dict, "ClientOptions"]
ResultTypes = Union[Optional[GraiType], Sequence[Optional[GraiType]]]
SegmentedCallerType = Callable[["BaseClient", Sequence, "ClientOptions"], List[T]]
ProtocolType = Union[Literal["http"], Literal["https"]]


class ClientOptions(BaseModel):
    payload: Dict = {}
    request_args: Dict = {}
    headers: Dict = {}
    query_args: Dict = {}

    @classmethod
    def __hash__(cls):
        return id(cls)

    def __add__(self, other: Union[Dict, "ClientOptions"]) -> "ClientOptions":
        if isinstance(other, Dict):
            other = ClientOptions(**other)
        elif not isinstance(other, ClientOptions):
            raise NotImplementedError(f"Unrecognized options type: {type(other)}")

        payload = self.payload | other.payload
        request_args = self.request_args | other.request_args
        headers = self.headers | other.headers
        query_args = self.query_args | other.query_args
        return ClientOptions(payload=payload, request_args=request_args, headers=headers, query_args=query_args)


def validate_connection_arguments(
    url: Optional[str] = None,
    host: Optional[str] = None,
    port: Optional[str] = None,
    protocol: Optional[ProtocolType] = None,
    insecure: Optional[bool] = None,
) -> Tuple[str, str, Optional[str], ProtocolType, bool]:
    if url is not None:
        # derive from url
        parsed_url = urlparse(url)
        url_protocol = parsed_url.scheme
        url_host = parsed_url.hostname
        url_port = str(parsed_url.port) if parsed_url.port is not None else None
        url_insecure = True if url_protocol == "http" else False

        if protocol is not None and url_protocol != protocol:
            message = (
                f"The provided url `{url}` uses the protocol {url_protocol}, but you've specified `protocol={protocol}`."
                f" Because these values differ we've defaulted to the protocol specified in the url"
            )
            warnings.warn(message)
        if host is not None and url_host != host:
            message = (
                f"The provided url `{url}` uses the host {url_host}, but you've specified `host={host}`."
                f" Because these values differ we've defaulted to the host specified in the url"
            )
            warnings.warn(message)
        if port is not None and url_port != port:
            message = (
                f"The provided url `{url}` uses the port {url_port} (which may come from it's protocol), but you've "
                f"specified `port={port}`. Because these values differ we've defaulted to the port "
                f"specified in the url"
            )
            warnings.warn(message)
        if insecure is not None and url_insecure != insecure:
            message = (
                f"The provided url `{url}` uses {'an insecure' if url_insecure else 'a secure'} connection, but you've "
                f"specified `insecure={insecure}`. Because these values differ we've defaulted to the security level "
                f"specified in the url."
            )
            warnings.warn(message)

        protocol = url_protocol
        host = url_host
        port = url_port
        insecure = url_insecure
    else:
        assert host, f"Client connections require at minimum a value for `url` or `host`."
        if port is None and host == "localhost":
            port = "8000"

        if protocol is None:
            protocol = "http" if insecure is True else "https"
            insecure = False if insecure is None else insecure
        else:
            # Protocol value was provided by the user
            if insecure is None:
                insecure = True if protocol == "http" else False
            else:
                # Both protocol and insecure values were provided by the user. Secure connections win.
                if not isinstance(insecure, bool):
                    message = f"Unexpected `insecure` value: {insecure}, `insecure` must be either True or False."
                    raise ValueError(message)
                if insecure is False and protocol == "http":
                    message = (
                        "By setting `insecure=False` you've requested a secure connection. However, it's "
                        "not possible to establish a secure connection using the http protocol. As a result "
                        "we've defaulted the protocol to https. To remove this warning either set "
                        "`insecure=True` or `protocol='https'`."
                    )
                    warnings.warn(message)
                    protocol = "https"
                elif insecure is True and protocol == "https":
                    message = (
                        "By setting `insecure=True` you've requested an insecure connection. However, it's not "
                        "possible to establish an insecure connection using the https protocol which is secure "
                        "by default. In order to protect your data we've defaulted to `insecure=False`. "
                        "To remove this warning either set `insecure=False` or `protocol='http'`."
                    )
                    warnings.warn(message)
                    insecure = False

        url = f"{protocol}://{host}"
        if port is not None:
            try:
                int(port)
            except:
                raise ValueError(f"Expected a valid integer value for `port` not {port}")
            url = f"{url}:{port}"

    if protocol not in ("http", "https", None):
        message = f"Unexpected `protocol` value: {protocol}, `protocol` must be one of 'http' or 'https'."
        raise ValueError(message)

    return url, host, port, protocol, insecure


class BaseClient(abc.ABC):
    id: Literal["base"] = "base"

    def __init__(
        self,
        host: Optional[str] = None,
        port: Optional[str] = None,
        protocol: Optional[ProtocolType] = None,
        insecure: Optional[bool] = None,
        url: Optional[str] = None,
        httpx_async_client_args: Optional[Union[Dict[str, Any], str]] = None,
    ):
        # TODO: Should require keyword arguments
        validated_args = validate_connection_arguments(url, host, port, protocol, insecure)
        if isinstance(httpx_async_client_args, str):
            httpx_async_client_args = json.loads(httpx_async_client_args)

        self.url: str = validated_args[0]
        self.host: str = validated_args[1]
        self.port: Optional[str] = validated_args[2]
        self.protocol: ProtocolType = validated_args[3]
        self.insecure: bool = validated_args[4]
        self.httpx_async_client_args: Dict[str, Any] = httpx_async_client_args

        self.default_payload: Dict[str, str] = dict()
        self.default_headers: Dict[str, str] = dict()
        self.default_request_args: Dict[str, str] = dict()
        self.default_query_args: Dict[str, str] = dict()

        self.session: Optional[httpx.AsyncClient] = None

        self.api: str = f"{self.url}"
        self.health_endpoint: str = f"{self.url}/health"
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

    @property
    def default_options(self) -> ClientOptions:
        return ClientOptions(
            **{
                "payload": self.default_payload,
                "headers": self.default_headers,
                "request_args": self.default_request_args,
                "query_args": self.default_query_args,
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

    async def session_manager(self, async_func: Callable, *args, options: Optional[OptionType] = None, **kwargs):
        if options is None:
            options = ClientOptions()

        options = self.default_options + options
        options.query_args |= kwargs

        async with self.get_session() as session:
            self.session = session
            result = await async_func(self, *args, options=options)
        self.session = None
        return result

    def get(self, *args, options: Optional[OptionType] = None, **kwargs):
        return asyncio.run(self.session_manager(get, *args, options=options, **kwargs))

    def post(self, *args, options: Optional[OptionType] = None, **kwargs):
        return asyncio.run(self.session_manager(post, *args, options=options, **kwargs))

    def patch(self, *args, options: Optional[OptionType] = None, **kwargs):
        return asyncio.run(self.session_manager(patch, *args, options=options, **kwargs))

    def delete(self, *args, options: Optional[OptionType] = None, **kwargs):
        return asyncio.run(self.session_manager(delete, *args, options=options, **kwargs))


# ----- Sequence Functions ----- #
def type_segmentation(objs: Sequence, priority_order) -> Tuple[List[int], Iterable[T]]:
    obj_idx_map = {}
    for idx, obj in enumerate(objs):
        obj_type = type(obj)
        obj_idx_map.setdefault(obj_type, [])
        obj_idx_map[obj_type].append(idx)

    for prioritized_type in priority_order:
        type_keys = [obj_type for obj_type in obj_idx_map.keys() if issubclass(obj_type, prioritized_type)]
        for obj_type in type_keys:
            idx = obj_idx_map.pop(obj_type)
            yield idx, (objs[i] for i in idx)

    for obj_type, idx in obj_idx_map.items():
        yield idx, (objs[i] for i in idx)


def segmented_caller(func: Callable, priority_order: Tuple = (Node, Edge)) -> SegmentedCallerType:
    async def inner(client: BaseClient, objs: Sequence[T], options: ClientOptions) -> List[T]:
        final_result = [None] * len(objs)
        for idx, iter_obj in type_segmentation(objs, priority_order):
            result = await asyncio.gather(*[func(client, obj, options=options) for obj in iter_obj])
            for i, obj in zip(idx, result):
                final_result[i] = obj
        return final_result

    return inner


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
    segmented_delete = segmented_caller(patch, priority_order=(Edge, Node))
    result = await segmented_delete(client, objs, options)
    return None


@post.register
async def post_sequence(
    client: BaseClient,
    objs: Sequence[T],
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    segmented_post = segmented_caller(post)
    result = await segmented_post(client, objs, options)
    return result


@patch.register
async def patch_sequence(
    client: BaseClient,
    objs: Sequence,
    options: ClientOptions = ClientOptions(),
) -> List[T]:
    segmented_patch = segmented_caller(patch)
    result = await segmented_patch(client, objs, options)
    return result


# -------------------------------------------- #


@get.register
async def client_get_url(client: BaseClient, url: str, options: ClientOptions = ClientOptions()) -> Response:
    headers = {**client.auth_headers, **options.headers}

    # if "workspace" in options.payload:
    #     url = add_query_params(url, {"workspace": options.payload["workspace"]})
    if options.query_args:
        url = add_query_params(url, options.query_args)
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
