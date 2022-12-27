import asyncio
import os
import random
import string
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    ParamSpec,
    Sequence,
    TypeVar,
)

import requests
from grai_source_fivetran.fivetran_api.api_models import (
    ColumnMetadataResponse,
    ConnectorResponse,
    GroupResponse,
    SchemaMetadataResponse,
    TableMetadataResponse,
    V1ConnectorsConnectorIdSchemasGetResponse,
    V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse,
    V1DestinationsDestinationIdGetResponse,
    V1GroupsGetResponse,
)

T = TypeVar("T")


def get_from_env(label: str, default: Optional[Any] = None, validator: Callable = None):
    package = "FIVETRAN"
    env_key = f"GRAI_{package}_{label.upper()}"
    result = os.getenv(env_key, default)
    if result is None:
        message = (
            f"Establishing {package} connection requires a {label}. "
            f"Either pass a value explicitly or set a {env_key} environment value."
        )
        raise Exception(message)
    return result if validator is None else validator(result)


def has_data_items(item: Dict) -> bool:
    if item.get("data", None) is None:
        return False
    elif item["data"].get("items", None) is None:
        return False
    else:
        return True


class FivetranConnector:
    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        fivetran_endpoint: str = "https://api.fivetran.com/v1/",
    ):
        self.base_endpoint = fivetran_endpoint.rstrip("/")
        self.user = user if user is not None else get_from_env("user")
        self.password = password if password is not None else get_from_env("password")

        self.session = requests.Session()
        self.session.auth = self.user, self.password
        self.default_headers = {"Accept": "application/json"}

    @staticmethod
    def get_cursor(k: Optional[int] = 10) -> str:
        k = 10 if k is None else k
        return "".join(random.choices(string.ascii_lowercase, k=k))

    def make_params(
        self, cursor_len: Optional[int] = None, limit: Optional[int] = None
    ):
        return {
            "cursor": self.get_cursor(cursor_len),
            "limit": 100 if limit is None else limit,
        }

    def make_request(
        self,
        request: Callable[..., requests.Response],
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs,
    ) -> Dict:
        headers = self.default_headers if headers is None else headers
        params = self.make_params() if params is None else params
        result = request(url, headers=headers, params=params, **kwargs)
        assert result.status_code == 200
        return result.json()

    def paginated_query(
        self,
        request: Callable[..., requests.Response],
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs,
    ) -> Iterable[Dict]:
        def has_cursor(item: Dict) -> bool:
            if (
                item.get("data", None) is not None
                and item["data"].get("nextCursor", None) is not None
            ):
                return True
            return False

        headers = self.default_headers if headers is None else headers
        params = self.make_params() if params is None else params
        result = self.make_request(
            request, url, headers=headers, params=params, **kwargs
        )
        yield result

        while has_cursor(result):
            params["cursor"] = result["data"]["nextCursor"]
            result = self.make_request(
                request, url, headers=headers, params=params, **kwargs
            )
            yield result

    def get_paginated_data_items(
        self,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> List[Dict]:
        query = self.paginated_query(
            self.session.get, url, params=params, headers=headers
        )
        data = (page["data"]["items"] for page in query if has_data_items(page))
        results = [item for items in data for item in items]
        return results

    def get_tables(
        self, connector_id: str, limit: Optional[int] = None
    ) -> List[TableMetadataResponse]:
        url = f"{self.base_endpoint}/metadata/connectors/{connector_id}/tables"
        return [
            TableMetadataResponse(**item)
            for item in self.get_paginated_data_items(
                url, params=self.make_params(limit=limit)
            )
        ]

    def get_columns(
        self, connector_id: str, limit: Optional[int] = None
    ) -> List[ColumnMetadataResponse]:
        url = f"{self.base_endpoint}/metadata/connectors/{connector_id}/columns"
        return [
            ColumnMetadataResponse(**item)
            for item in self.get_paginated_data_items(
                url, params=self.make_params(limit=limit)
            )
        ]

    def get_schemas(
        self, connector_id: str, limit: Optional[int] = None
    ) -> List[SchemaMetadataResponse]:
        url = f"{self.base_endpoint}/metadata/connectors/{connector_id}/schemas"
        return [
            SchemaMetadataResponse(**item)
            for item in self.get_paginated_data_items(
                url, params=self.make_params(limit=limit)
            )
        ]

    def get_all_groups(self, limit: Optional[int] = None) -> List[GroupResponse]:
        url = f"{self.base_endpoint}/groups"
        return [
            GroupResponse(**item)
            for item in self.get_paginated_data_items(
                url, params=self.make_params(limit=limit)
            )
        ]

    def get_group_connectors(
        self, group_id: str, limit: Optional[int] = None
    ) -> List[ConnectorResponse]:
        url = f"{self.base_endpoint}/groups/{group_id}/connectors"
        return [
            ConnectorResponse(**item)
            for item in self.get_paginated_data_items(
                url, params=self.make_params(limit=limit)
            )
        ]

    def get_destination_metadata(
        self, destination_id: str
    ) -> V1DestinationsDestinationIdGetResponse:
        url = f"{self.base_endpoint}/destinations/{destination_id}"
        data = self.make_request(self.session.get, url)
        return V1DestinationsDestinationIdGetResponse(**data)

    def get_connector_metadata(
        self, connector_id: str
    ) -> V1ConnectorsConnectorIdSchemasGetResponse:
        url = f"{self.base_endpoint}/connectors/{connector_id}/schemas"
        data = self.make_request(self.session.get, url)
        return V1ConnectorsConnectorIdSchemasGetResponse(**data)

    def get_source_table_column_metadata(
        self, connector_id: str, schema: str, table: str
    ) -> V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse:
        url = f"{self.base_endpoint}/connectors/{connector_id}/schemas/{schema}/tables/{table}/columns"
        data = self.make_request(self.session.get, url)
        return V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse(**data)


async def caller(
    semaphore: asyncio.Semaphore, func: Callable[..., T], *args, **kwargs
) -> T:
    result = func(*args, **kwargs)

    async with semaphore:
        if semaphore.locked():
            await asyncio.sleep(1)
    return result


def parallelize_http(semaphore):
    async def parallel(
        func: Callable[P, Sequence[T]],
        arg_list: Iterable[Sequence[Any]],
        kwarg_list: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> List[T]:
        arg_list = list(arg_list)
        kwarg_list = [{}] * len(arg_list) if kwarg_list is None else kwarg_list
        assert len(arg_list) == len(kwarg_list)

        tasks = (
            caller(semaphore, func, *args, **kwargs)
            for args, kwargs in zip(arg_list, kwarg_list)
        )
        return await asyncio.gather(*tasks)

    def inner(
        func: Callable[P, Sequence[T]],
        arg_list: Iterable[Sequence[Any]],
        kwarg_list: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> List[T]:
        return asyncio.run(parallel(func, arg_list, kwarg_list))

    return inner


class FivetranGraiMapper(FivetranConnector):
    def __init__(self, parallelization: int = 10):
        self.parallelization = parallelization
        self.semaphore = asyncio.Semaphore(self.parallelization)
        self.http_runner = parallelize_http(self.semaphore)

        self.groups = {
            group.id: group for group in self.get_all_groups() if group.id is not None
        }
        self.connectors = {
            conn.id: conn
            for group_id in self.groups.keys()
            for conn in self.get_group_connectors(group_id)
            if conn.id is not None
        }

        schemas = self.http_runner(self.get_schemas, arg_list=self.connectors.keys())
        tables = self.http_runner(self.get_tables, arg_list=self.connectors.keys())
        columns = self.http_runner(self.get_columns, arg_list=self.connectors.keys())

        self.schemas: Dict[str, SchemaMetadataResponse] = {
            item.id: item for seq in schemas for item in seq
        }
        self.tables: Dict[str, TableMetadataResponse] = {
            item.id: item for seq in tables for item in seq
        }
        self.columns: Dict[str, ColumnMetadataResponse] = {
            item.id: item for seq in columns for item in seq
        }

    def get_nodes_and_edges(self):
        pass
