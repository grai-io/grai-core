import asyncio
import json
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
from pydantic import BaseModel, BaseSettings, Json, SecretStr, validator

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
from grai_source_fivetran.models import (
    Column,
    Edge,
    NamespaceIdentifier,
    NodeTypes,
    Table,
)

T = TypeVar("T")
P = ParamSpec("P")


class FiveTranConfig(BaseSettings):
    """ """

    endpoint: str = "https://api.fivetran.com/v1"
    api_key: SecretStr
    api_secret: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, value):
        """

        Args:
            value:

        Returns:

        Raises:

        """
        return value.rstrip("/")

    class Config:
        """ """

        env_prefix = "grai_fivetran_"
        env_file = ".env"


def has_data_items(item: Dict) -> bool:
    """

    Args:
        item (Dict):

    Returns:

    Raises:

    """
    if item.get("data", None) is None:
        return False
    elif item["data"].get("items", None) is None:
        return False
    else:
        return True


class FivetranAPI:
    """ """

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
    ) -> Tuple[Dict, requests.Response]:
        """

        Args:
            request:
            url:
            headers:  (Default value = None)
            params:  (Default value = None)
            **kwargs:

        Returns:

        Raises:

        """
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
        """

        Args:
            request:
            url:
            headers:  (Default value = None)
            params:  (Default value = None)
            **kwargs:

        Returns:

        Raises:

        """

        def has_cursor(item: Dict) -> bool:
            """

            Args:
                item):

            Returns:

            Raises:

            """
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
        """

        Args:
            url:
            headers:  (Default value = None)
            params:  (Default value = None)

        Returns:

        Raises:

        """
        query = self.paginated_query(self.session.get, url, params=params, headers=headers)
        data = (page["data"]["items"] for page in query if has_data_items(page))
        results = [item for items in data for item in items]
        return results

    def get_tables(self, connector_id: str, limit: Optional[int] = None) -> List[TableMetadataResponse]:
        """

        Args:
            connector_id:
            limit:  (Default value = None)

        Returns:

        Raises:

        """
        url = f"{self.config.endpoint}/metadata/connectors/{connector_id}/tables"
        return [TableMetadataResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_columns(self, connector_id: str, limit: Optional[int] = None) -> List[ColumnMetadataResponse]:
        """

        Args:
            connector_id:
            limit:  (Default value = None)

        Returns:

        Raises:

        """
        url = f"{self.config.endpoint}/metadata/connectors/{connector_id}/columns"
        return [ColumnMetadataResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_schemas(self, connector_id: str, limit: Optional[int] = None) -> List[SchemaMetadataResponse]:
        """

        Args:
            connector_id:
            limit:  (Default value = None)

        Returns:

        Raises:

        """
        url = f"{self.config.endpoint}/metadata/connectors/{connector_id}/schemas"
        return [SchemaMetadataResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_all_groups(self, limit: Optional[int] = None) -> List[GroupResponse]:
        """

        Args:
            limit:  (Default value = None)

        Returns:

        Raises:

        """
        url = f"{self.config.endpoint}/groups"
        return [GroupResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_group_connectors(self, group_id: str, limit: Optional[int] = None) -> List[ConnectorResponse]:
        """

        Args:
            group_id:
            limit:  (Default value = None)

        Returns:

        Raises:

        """
        url = f"{self.config.endpoint}/groups/{group_id}/connectors"
        return [ConnectorResponse(**item) for item in self.get_paginated_data_items(url)]

    def get_destination_metadata(self, destination_id: str) -> V1DestinationsDestinationIdGetResponse:
        """

        Args:
            destination_id (str):

        Returns:

        Raises:

        """
        url = f"{self.config.endpoint}/destinations/{destination_id}"
        data, response = self.make_request(self.session.get, url)
        return V1DestinationsDestinationIdGetResponse(**data)

    def get_connector_metadata(self, connector_id: str) -> V1ConnectorsConnectorIdSchemasGetResponse:
        """

        Args:
            connector_id (str):

        Returns:

        Raises:

        """
        url = f"{self.config.endpoint}/connectors/{connector_id}/schemas"
        data, response = self.make_request(self.session.get, url)
        return V1ConnectorsConnectorIdSchemasGetResponse(**data)

    def get_source_table_column_metadata(
        self, connector_id: str, schema: str, table: str
    ) -> V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse:
        """

        Args:
            connector_id (str):
            schema (str):
            table (str):

        Returns:

        Raises:

        """
        url = f"{self.config.endpoint}/connectors/{connector_id}/schemas/{schema}/tables/{table}/columns"
        data, response = self.make_request(self.session.get, url)
        return V1ConnectorsConnectorIdSchemasSchemaTablesTableColumnsGetResponse(**data)

    def get_connectors(self) -> List[ConnectorResponse]:
        """

        Args:

        Returns:

        Raises:

        """
        groups = {group.id: group for group in self.get_all_groups() if group.id is not None}
        connectors = [conn for group_id in groups.keys() for conn in self.get_group_connectors(group_id)]
        return connectors


async def caller(semaphore: asyncio.Semaphore, func: Callable[..., T], *args, **kwargs) -> T:
    """

    Args:
        semaphore (asyncio.Semaphore):
        func (Callable[..., T]):
        *args:
        **kwargs:

    Returns:

    Raises:

    """
    result = func(*args, **kwargs)

    async with semaphore:
        if semaphore.locked():
            await asyncio.sleep(1)
    return result


def parallelize_http(semaphore):
    """

    Args:
        semaphore:

    Returns:

    Raises:

    """

    async def parallel(
        func: Callable[P, T],
        arg_list: Iterable[Sequence[Any]],
        kwarg_list: Optional[Sequence[Dict[str, Any]]] = None,
    ) -> Tuple[T]:
        """

        Args:
            func (Callable[P, T]):
            arg_list (Iterable[Sequence[Any]]):
            kwarg_list (Optional[Sequence[Dict[str, Any]]], optional):  (Default value = None)

        Returns:

        Raises:

        """
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
        """

        Args:
            func (Callable[P, T]):
            arg_list (Iterable[Sequence[Any]]):
            kwarg_list (Optional[Sequence[Dict[str, Any]]], optional):  (Default value = None)

        Returns:

        Raises:

        """
        return asyncio.run(parallel(func, arg_list, kwarg_list))

    return inner


class SourceDestinationDict(TypedDict):
    """ """

    source: str
    destination: str


NamespaceTypes = Union[Dict[str, Union[str, SourceDestinationDict]], str]


def process_base_namespace_map(
    namespace_map: Optional[Union[str, Dict[str, Union[str, SourceDestinationDict]]]]
) -> Dict[str, NamespaceIdentifier]:
    if namespace_map is None:
        namespace_map = {}
    elif isinstance(namespace_map, str):
        try:
            namespace_map = json.loads(namespace_map)
        except:
            message = f"The provided JSON string was invalid and could not be successfully parsed."
            raise Exception(message)
    elif isinstance(namespace_map, dict):
        message = (
            "The namespaces object should be a dictionary whose id's are Fivetran connector id's and whose values "
            "identify the Grai namespace associated with either the source or destination of the connector. "
            "The values can either be provided as a dictionary with the keys 'source' and 'destination' or ",
            "as strings identifying the Grai namespace you'd like to associate with both the source "
            "and destination.",
        )
        assert all(isinstance(v, (dict, str)) for v in namespace_map.values()), message
        assert all("source" in v and "destination" in v for v in namespace_map.values() if isinstance(v, dict)), message
    else:
        raise ValueError(f"namespace_map must be either a JSON string, a dictionary not {type(namespace_map)}")

    result: Dict[str, NamespaceIdentifier] = {}

    for k, v in namespace_map.items():
        result[k] = NamespaceIdentifier(source=v, destination=v) if isinstance(v, str) else NamespaceIdentifier(**v)

    return result


class FivetranConnector(FivetranAPI):
    """ """

    def __init__(
        self,
        namespaces: Optional[NamespaceTypes] = None,
        default_namespace: Optional[str] = None,
        parallelization: int = 10,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self.parallelization = parallelization
        self.semaphore = asyncio.Semaphore(self.parallelization)
        self.http_runner = parallelize_http(self.semaphore)
        self.default_namespace = default_namespace
        self._namespace_map_base = process_base_namespace_map(namespaces)

        self._namespace_map: Optional[Dict[str, NamespaceIdentifier]] = None
        self._connectors: Optional[Dict[str, ConnectorResponse]] = None

        self.table_to_conn_map: Dict[str, str] = {}
        self.column_to_conn_map: Dict[str, str] = {}
        self.schemas: Dict[str, SchemaMetadataResponse] = {}
        self.tables: Dict[str, TableMetadataResponse] = {}
        self.columns: Dict[str, ColumnMetadataResponse] = {}

        self._nodes = None
        self._edges = None
        self.lineage_ready = False

    def has_query_permissions(self):
        try:
            # Should check all of the required endpoints here since the API key can be scoped
            self.get_all_groups(limit=1)
            return True
        except Exception as e:
            return False

    @property
    def connectors(self) -> Dict[str, ConnectorResponse]:
        if self._connectors is None:
            self._connectors = {conn.id: conn for conn in self.get_connectors() if conn.id is not None}
        return self._connectors

    @property
    def namespace_map(self):
        if self._namespace_map is None:
            namespace_map = self._namespace_map_base.copy()  # avoid modifying the users original argument
            if self.default_namespace is not None:
                identifier = NamespaceIdentifier(source=self.default_namespace, destination=self.default_namespace)
                for k in self.connectors.keys():
                    namespace_map.setdefault(k, identifier.copy())
            else:
                for k in self.connectors.keys():
                    source_namespace = f"fivetran-{k}-source"
                    destination_namespace = f"fivetran-{k}-destination"
                    identifier = NamespaceIdentifier(source=source_namespace, destination=destination_namespace)
                    namespace_map.setdefault(k, identifier)
            self._namespace_map = namespace_map

        return self._namespace_map

    def build_lineage(self):
        """ """
        connector_ids = [[conn_id] for conn_id in self.connectors.keys()]
        schemas = self.http_runner(self.get_schemas, arg_list=connector_ids)
        tables = self.http_runner(self.get_tables, arg_list=connector_ids)
        columns = self.http_runner(self.get_columns, arg_list=connector_ids)

        for conn_id, t_res, c_res in zip(self.connectors.keys(), tables, columns):
            for table in t_res:
                self.table_to_conn_map.setdefault(table.id, conn_id)
            for column in c_res:
                self.column_to_conn_map.setdefault(column.id, conn_id)

        self.schemas.update({item.id: item for seq in schemas for item in seq})
        self.tables.update({item.id: item for seq in tables for item in seq})
        self.columns.update({item.id: item for seq in columns for item in seq})

    def get_nodes_and_edges(self) -> Tuple[List[NodeTypes], List[Edge]]:
        """

        Args:

        Returns:

        Raises:

        """
        if self.lineage_ready:
            return self._nodes, self._edges

        self.build_lineage()

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

        self._nodes = list(chain(chain.from_iterable(tables.values()), *columns))
        self._edges = list(chain(column_edges, table_edges, table_to_column_edges))
        self.lineage_ready = True

        return self._nodes, self._edges
