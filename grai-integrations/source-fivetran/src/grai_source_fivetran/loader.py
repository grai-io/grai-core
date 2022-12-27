import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union, Iterable, Tuple, TypeVar, Sequence
import requests
from functools import partial
import string
import random
import asyncio
from pydantic import BaseModel
from grai_source_fivetran.models import (
    TableResult,
    ColumnResult,
    SchemaResult,
    DestinationMetadata,
    ConnectorMetadata,
    SourceTableColumnMetadata,
)
from grai_source_fivetran.fivetran_api.api_models import (
    V1ConnectorsConnectorIdSchemasGetResponse,
    V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse,
    V1DestinationsDestinationIdGetResponse,
    V1MetadataConnectorsConnectorIdSchemasGetResponse,
    SchemaMetadataResponse,
    V1MetadataConnectorsConnectorIdColumnsGetResponse,
    ColumnMetadataResponse,
    V1MetadataConnectorsConnectorIdTablesGetResponse,
    TableMetadataResponse,
    V1GroupsGetResponse,
    GroupResponse,
    V1GroupsGroupIdConnectorsGetResponse,
    ConnectorResponse,
)

T = TypeVar('T')
R = TypeVar('R')


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


def unpack(items: Sequence[Sequence[T]]) -> Sequence[T]:
    return [item for seq in items for item in seq]


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

        self.sessions = requests.Session()
        self.sessions.auth = self.auth
        self.default_headers = {"Accept": "application/json"}
        self.default_params = {"cursor": self.get_cursor(), "limit": 100}

    @staticmethod
    def get_cursor() -> str:
        return "".join(random.choices(string.ascii_lowercase, k=10))

    @staticmethod
    def make_request(
        request: Callable[..., requests.Response],
        url: str,
        headers: Dict,
        params: Dict,
        **kwargs,
    ) -> Dict:
        result = request(url, headers=headers, params=params, **kwargs)
        assert result.status_code == 200
        return result.json()

    def make_params(self, limit: int = 100):
        return {"cursor": self.get_cursor(), "limit": limit}

    def paginated_query(
        self,
        request: Callable[..., requests.Response],
        result_obj: T,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs,
    ) -> Iterable[T]:
        headers = self.default_headers if headers is None else headers
        params = self.make_params() if params is None else params
        result = self.make_request(
            request, url, headers=headers, params=params, **kwargs
        )
        yield result_obj(**result)

        while "nextCursor" in result["data"]:
            params["cursor"] = result.data.nextCursor
            result = self.make_request(
                request, url, headers=headers, params=params, **kwargs
            )
            yield result_obj(**result)

    def get_paginated_data_items(self, url: str, result_obj: T, headers: Optional[Dict] = None, params: Optional[Dict] = None) -> List[R]:
        results = []
        for page in self.paginated_query(self.session.get, result_obj, url, params=params, headers=headers):
            results.extend(page.data.items)
        return results

    def get_tables(self, connector_id: str, limit: int = 0) -> List[TableMetadataResponse]:
        url = f"{self.base_endpoint}/metadata/connectors/{connector_id}/tables"
        result_type = V1MetadataConnectorsConnectorIdTablesGetResponse
        results = self.get_paginated_data_items(url, result_type, params=self.make_params(limit))
        return results

    def get_columns(self, connector_id: str, limit: int = 0) -> List[ColumnMetadataResponse]:
        url = f"{self.base_endpoint}/metadata/connectors/{connector_id}/columns"
        result_type = V1MetadataConnectorsConnectorIdColumnsGetResponse
        results = self.get_paginated_data_items(url, result_type, params=self.make_params(limit))
        return results

    def get_schemas(self, connector_id: str, limit: int = 0) -> List[SchemaMetadataResponse]:
        url = f"{self.base_endpoint}/metadata/connectors/{connector_id}/schemas"
        result_type = V1MetadataConnectorsConnectorIdSchemasGetResponse
        results = self.get_paginated_data_items(url, result_type, params=self.make_params(limit))
        return results

    def get_destination_metadata(self, destination_id: str) -> V1DestinationsDestinationIdGetResponse:
        url = f"{self.base_endpoint}/destinations/{destination_id}"
        data = self.make_request(self.session.get, url)
        return V1DestinationsDestinationIdGetResponse(**data)

    def get_connector_metadata(self, connector_id: str) -> V1ConnectorsConnectorIdSchemasGetResponse:
        url = f"{self.base_endpoint}/connectors/{connector_id}/schemas"
        data = self.make_request(self.session.get, url)
        return V1ConnectorsConnectorIdSchemasGetResponse(**data)

    def get_source_table_column_metadata(
        self, connector_id: str, schema: str, table: str
    ) -> V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse:
        url = f"{self.base_endpoint}/connectors/{connector_id}/schemas/{schema}/tables/{table}/columns"
        data = self.make_request(self.session.get, url)
        return V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse(**data)

    def get_all_groups(self, limit: int = 0) -> List[GroupResponse]:
        url = f"{self.base_endpoint}/groups"
        result_type = V1GroupsGetResponse
        results = self.get_paginated_data_items(url, result_type, params=self.make_params(limit))
        return results

    def get_group_connectors(self, group_id: str, limit: int = 0) -> List[ConnectorResponse]:
        url = f"{self.base_endpoint}/groups/{group_id}/connectors"
        result_type = V1GroupsGroupIdConnectorsGetResponse
        results = self.get_paginated_data_items(url, result_type, params=self.make_params(limit))
        return results


class FivetranGraiMapper(FivetranConnector):
    def __init__(self, parallelization: int = 10):
        self.parallelization = parallelization
        self.request_limiter = asyncio.Semaphore(self.parallelization)

        self.groups = self.get_all_groups()
        self.connectors = {conn.id: conn for group in self.groups for conn in self.get_group_connectors(group)}

        self.schemas = unpack(self.parallel(self.get_schemas, arg_list=self.connectors.keys()))
        self.tables = unpack(self.parallel(self.get_tables, arg_list=self.connectors.keys()))
        self.columns = unpack(self.parallel(self.get_columns, arg_list=self.connectors.keys()))

    async def caller(self, func: Callable[..., T], *args, **kwargs) -> T:
        result = func(*args, **kwargs)

        async with self.request_limiter:
            if self.request_limiter.locked():
                await asyncio.sleep(1)
        return result

    async def parallel(self, func: Callable[..., T], arg_list: Sequence, kwarg_list: Optional[List[Dict]] = None) -> List[T]:
        if kwarg_list is None:
            kwarg_list = [{}] * len(arg_list)
        assert len(arg_list) == len(kwarg_list)

        tasks = (self.caller(func, *args, **kwargs) for args, kwargs in zip(arg_list, kwarg_list))
        return await asyncio.gather(*tasks)

    def get_nodes_and_edges(self):
        pass

