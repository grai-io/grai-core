import asyncio
from itertools import chain
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    ParamSpec,
    Sequence,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
)

import requests
from pydantic import BaseModel, BaseSettings, SecretStr, validator

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
from grai_source_fivetran.models import Column, Edge, NamespaceIdentifier, Table

T = TypeVar("T")
P = ParamSpec("P")


class FiveTranConfig(BaseSettings):
    endpoint: str = "https://api.fivetran.com/v1"
    api_key: SecretStr
    api_secret: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, value):
        return value.rstrip("/")

    class Config:
        env_prefix = "grai_fivetran_"
        env_file = ".env"


def has_data_items(item: Dict) -> bool:
    if item.get("data", None) is None:
        return False
    elif item["data"].get("items", None) is None:
        return False
    else:
        return True


class FivetranAPI:
    def __init__(
        self,
        api_key: Optional[str] = None,
        api_secret: Optional[str] = None,
        endpoint: Optional[str] = None,
        limit: Optional[int] = None,
    ):
        passthrough_kwargs = {
            "api_key": api_key,
            "api_secret": api_secret,
            "endpoint": endpoint,
        }
        self.config = FiveTranConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})

        self.session = requests.Session()
        self.session.auth = (
            self.config.api_key.get_secret_value(),
            self.config.api_secret.get_secret_value(),
        )
        self.session.headers.update({"Accept": "application/json"})
        self.session.params.update({"limit": 10000 if limit is None else limit})

    def make_request(
        self,
        request: Callable[..., requests.Response],
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs,
    ) -> Dict:
        params = self.session.params if params is None else {**self.session.params, **params}
        headers = self.session.headers if headers is None else {**self.session.headers, **headers}
        result = request(url, params=params, headers=headers, **kwargs)
        assert result.status_code == 200
        return result.json(), result

    def paginated_query(
        self,
        request: Callable[..., requests.Response],
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
        **kwargs,
    ) -> Iterable[Dict]:
        def has_cursor(item: Dict) -> bool:
            if item.get("data", {}).get("nextCursor", None) is not None:
                return True
            return False

        result, response = self.make_request(request, url, headers=headers, params=params, **kwargs)
        yield result

        while has_cursor(result):
            params = {**response.request.params, "cursor": result["data"]["nextCursor"]}
            result, response = self.make_request(request, url, headers=headers, params=params, **kwargs)
            yield result

    def get_paginated_data_items(
        self,
        url: str,
        headers: Optional[Dict] = None,
        params: Optional[Dict] = None,
    ) -> List[Dict]:
        query = self.paginated_query(self.session.get, url, params=params, headers=headers)
        data = (page["data"]["items"] for page in query if has_data_items(page))
        results = [item for items in data for item in items]
        return results

    def get_tables(self, connector_id: str, limit: Optional[int] = None) -> List[TableMetadataResponse]:
        url = f"{self.config.endpoint}/metadata/connectors/{connector_id}/tables"
        return [TableMetadataResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_columns(self, connector_id: str, limit: Optional[int] = None) -> List[ColumnMetadataResponse]:
        url = f"{self.config.endpoint}/metadata/connectors/{connector_id}/columns"
        return [ColumnMetadataResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_schemas(self, connector_id: str, limit: Optional[int] = None) -> List[SchemaMetadataResponse]:
        url = f"{self.config.endpoint}/metadata/connectors/{connector_id}/schemas"
        return [SchemaMetadataResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_all_groups(self, limit: Optional[int] = None) -> List[GroupResponse]:
        url = f"{self.config.endpoint}/groups"
        return [GroupResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_group_connectors(self, group_id: str, limit: Optional[int] = None) -> List[ConnectorResponse]:
        url = f"{self.config.endpoint}/groups/{group_id}/connectors"
        return [ConnectorResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_destination_metadata(self, destination_id: str) -> V1DestinationsDestinationIdGetResponse:
        url = f"{self.config.endpoint}/destinations/{destination_id}"
        data, response = self.make_request(self.session.get, url)
        return V1DestinationsDestinationIdGetResponse(**data)

    def get_connector_metadata(self, connector_id: str) -> V1ConnectorsConnectorIdSchemasGetResponse:
        url = f"{self.config.endpoint}/connectors/{connector_id}/schemas"
        data, response = self.make_request(self.session.get, url)
        return V1ConnectorsConnectorIdSchemasGetResponse(**data)

    def get_source_table_column_metadata(
        self, connector_id: str, schema: str, table: str
    ) -> V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse:
        url = f"{self.config.endpoint}/connectors/{connector_id}/schemas/{schema}/tables/{table}/columns"
        data, response = self.make_request(self.session.get, url)
        return V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse(**data)


async def caller(semaphore: asyncio.Semaphore, func: Callable[..., T], *args, **kwargs) -> T:
    result = func(*args, **kwargs)

    async with semaphore:
        if semaphore.locked():
            await asyncio.sleep(1)
    return result


def parallelize_http(semaphore):
    async def parallel(
        func: Callable[P, T],
        arg_list: Iterable[Sequence[Any]],
        kwarg_list: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> Tuple[T]:
        arg_list = list(arg_list) if not isinstance(arg_list, list) else arg_list
        kwarg_list = [{}] * len(arg_list) if kwarg_list is None else kwarg_list
        assert len(arg_list) == len(kwarg_list)
        tasks = (caller(semaphore, func, *args, **kwargs) for args, kwargs in zip(arg_list, kwarg_list))
        return await asyncio.gather(*tasks)

    def inner(
        func: Callable[P, T],
        arg_list: Iterable[Sequence[Any]],
        kwarg_list: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> List[T]:
        return asyncio.run(parallel(func, arg_list, kwarg_list))

    return inner


class SourceDestinationDict(TypedDict):
    source: str
    destination: str


NamespaceTypes = Union[Dict[str, str], SourceDestinationDict]


class FivetranConnector(FivetranAPI):
    def __init__(
        self,
        namespaces: Optional[NamespaceTypes] = None,
        default_namespace: Optional[str] = None,
        parallelization: int = 10,
        *args,
        **kwargs,
    ):
        if namespaces is None and default_namespace is None:
            message = (
                f"The FivetranGraiMapper requires a not null value for `default_namespace` and/or `namespaces. "
                f"These values are used to identify which Fivetran connection id's belong to which associated "
                f"Grai namespace. `default_namespace` will map a single namespace to ALL connection id's."
                "This behavior can be overridden by `namespaces` which maps {connection_id -> "
                "namespace} or {connection_id -> {source: namespace, destination: namespace}}"
            )
            raise ValueError(message)
        elif namespaces is not None:
            assert all(isinstance(v, (dict, str)) for v in namespaces.values())
            assert all(isinstance(v, SourceDestinationDict) for v in namespaces.values() if isinstance(v, dict))
        else:
            namespaces = {}

        super().__init__(*args, **kwargs)
        self.parallelization = parallelization
        self.semaphore = asyncio.Semaphore(self.parallelization)
        self.http_runner = parallelize_http(self.semaphore)

        self.groups = {group.id: group for group in self.get_all_groups() if group.id is not None}
        self.connectors = {
            conn.id: conn
            for group_id in self.groups.keys()
            for conn in self.get_group_connectors(group_id)
            if conn.id is not None
        }

        if default_namespace is None:
            self.connectors = {k: v for k, v in self.connectors.items() if v in namespaces}
        else:
            namespaces = {**namespaces}  # avoid modifying the users original argument
            for k in self.connectors.keys():
                namespaces.setdefault(k, default_namespace)

        self.namespace_map = {
            k: NamespaceIdentifier(source=v, destination=v) if isinstance(v, str) else NamespaceIdentifier(**v)
            for k, v in namespaces.items()
        }

        connector_ids = [[conn_id] for conn_id in self.connectors.keys()]
        schemas = self.http_runner(self.get_schemas, arg_list=connector_ids)
        tables = self.http_runner(self.get_tables, arg_list=connector_ids)
        columns = self.http_runner(self.get_columns, arg_list=connector_ids)

        self.table_to_conn_map = {}
        self.column_to_conn_map = {}
        for conn_id, t_res, c_res in zip(self.connectors.keys(), tables, columns):
            for table in t_res:
                self.table_to_conn_map.setdefault(table.id, conn_id)
            for column in c_res:
                self.column_to_conn_map.setdefault(column.id, conn_id)

        self.schemas: Dict[str, SchemaMetadataResponse] = {item.id: item for seq in schemas for item in seq}
        self.tables: Dict[str, TableMetadataResponse] = {item.id: item for seq in tables for item in seq}
        self.columns: Dict[str, ColumnMetadataResponse] = {item.id: item for seq in columns for item in seq}

    def get_nodes_and_edges(self):
        # table.parent_id -> schema.id
        # column.parent_id -> table.id
        tables = {
            table.id: Table.from_fivetran_models(
                self.schemas[table.parent_id],
                table,
                self.namespace_map[self.table_to_conn_map[table.id]],
            )
            for table in self.tables.values()
        }
        columns = [
            Column.from_fivetran_models(
                self.schemas[self.tables[column.parent_id].parent_id],
                self.tables[column.parent_id],
                column,
                self.namespace_map[self.column_to_conn_map[column.id]],
            )
            for column in self.columns.values()
        ]

        column_edges = (Edge(source=c1, destination=c2, constraint_type="c") for c1, c2 in columns)
        table_edges = (Edge(source=t1, destination=t2, constraint_type="c") for t1, t2 in tables.values())
        table_to_column_edges = (
            Edge(source=table, destination=col, constraint_type="bt")
            for cols in columns
            for col, table in zip(cols, tables[cols[0].fivetran_table_id])
        )

        nodes = chain(chain.from_iterable(tables.values()), *columns)
        edges = chain(column_edges, table_edges, table_to_column_edges)
        return list(nodes), list(edges)
