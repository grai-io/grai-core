import json
import os
from datetime import datetime, timedelta, timezone
from functools import cache, cached_property, lru_cache
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

from google.cloud import bigquery, logging
from google.oauth2 import service_account

from grai_source_bigquery.models import (
    BigqueryNode,
    Column,
    Constraint,
    Edge,
    Table,
    TableID,
)


def get_from_env(
    label: str,
    default: Optional[Any] = None,
    required: bool = True,
    validator: Optional[Callable] = None,
):
    """

    Args:
        label (str):
        default (Optional[Any], optional):  (Default value = None)
        required (bool, optional):  (Default value = True)
        validator (Optional[Callable], optional):  (Default value = None)

    Returns:

    Raises:

    """
    env_key = f"GRAI_BIGQUERY_{label.upper()}"
    result = os.getenv(env_key, default)
    if result is None and required:
        message = (
            f"Establishing bigquery connection requires a {label}. "
            f"Either pass a value explicitly or set a {env_key} environment value."
        )
        raise Exception(message)
    return result if validator is None else validator(result)


class BigqueryConnector:
    """ """

    def __init__(
        self,
        namespace: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[Union[str, List[str]]] = None,
        credentials: Optional[str] = None,
        **kwargs,
    ):
        self.namespace = get_from_env("namespace", "default") if namespace is None else namespace
        self.project = get_from_env("project", required=False) if project is None else project
        self.dataset = get_from_env("dataset", required=False) if dataset is None else dataset
        self.datasets = [self.dataset] if isinstance(self.dataset, str) else self.dataset

        self.credentials = get_from_env("credentials", required=False) if credentials is None else credentials
        self._connection: Optional[bigquery.connector.BigqueryConnection] = None

        self._tables: Optional[List[Table]] = None
        self._foreign_keys: Optional[List[Edge]] = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self) -> "BigqueryConnector":
        """

        Args:

        Returns:

        Raises:

        """
        if self._connection is None:
            credentials = None

            if self.credentials:
                json_acct_info = json.loads(self.credentials, strict=False)
                credentials = service_account.Credentials.from_service_account_info(json_acct_info)

            self._connection = bigquery.Client(credentials=credentials, project=self.project)
        return self

    @property
    def connection(self) -> bigquery.Client:
        """

        Args:

        Returns:

        Raises:

        """
        if self._connection is None:
            raise Exception("Not connected, call `.connect()")
        return self._connection

    def close(self) -> None:
        """

        Args:

        Returns:

        Raises:

        """
        self.connection.close()
        self._connection = None

    def query_runner(self, query: str, param_dict: Dict = {}) -> List[Dict]:
        """

        Args:
            query (str):
            param_dict (Dict, optional):  (Default value = {})

        Returns:

        Raises:

        """
        return self.connection.query(query)

    @lru_cache
    def tables(self, dataset: str) -> List[Table]:
        """Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.

        Args:

        Returns:

        Raises:

        """
        query = f"""
            SELECT table_schema, table_name, table_type
            FROM {self.project}.{dataset}.INFORMATION_SCHEMA.TABLES
            WHERE table_schema != 'INFORMATION_SCHEMA'
            ORDER BY table_schema, table_name
        """
        res = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))

        additional_args = {
            "namespace": self.namespace,
            "table_dataset": dataset,
        }

        tables = [Table(**result, **additional_args) for result in res]
        for table in tables:
            table.columns = self.get_table_columns(table, dataset)
        return tables

    @lru_cache
    def columns(self, dataset: str) -> List[Column]:
        """Creates and returns a list of dictionaries for the specified
        schema.table in the database connected to.

        Args:

        Returns:

        Raises:

        """

        query = f"""
            SELECT column_name, data_type, is_nullable, column_default, table_schema, table_name
            FROM {self.project}.{dataset}.INFORMATION_SCHEMA.COLUMNS
        """

        res = [{k.lower(): v for k, v in result.items()} for result in self.query_runner(query)]
        for item in res:
            item.update(
                {
                    "table": item["table_name"],
                    "column_schema": item["table_schema"],
                }
            )

        addtl_args = {
            "namespace": self.namespace,
        }
        return [Column(**result, **addtl_args) for result in res]

    @lru_cache
    def column_map(self, dataset: str) -> Dict[Tuple[str, str], List[Column]]:
        """

        Args:

        Returns:

        Raises:

        """
        result_map: Dict[Tuple[str, str], List[Column]] = {}
        for col in self.columns(dataset):
            table_id = (col.column_schema, col.table)
            result_map.setdefault(table_id, [])
            result_map[table_id].append(col)
        return result_map

    def get_table_columns(self, table: Table, dataset: str) -> List[Column]:
        """

        Args:
            table (Table):

        Returns:

        Raises:

        """
        table_id = (table.table_schema, table.name)

        column_map = self.column_map(dataset)

        if table_id in column_map:
            return column_map[table_id]

        schema = table_id[0]
        name = table_id[1]
        table_id = (schema, name)
        if table_id in column_map:
            return column_map[table_id]
        else:
            raise Exception(f"No columns found for table with schema={schema} and name={name}")

    def get_nodes(self, dataset: str) -> List[BigqueryNode]:
        """

        Args:

        Returns:

        Raises:

        """
        return list(chain(self.tables(dataset), self.columns(dataset)))

    def get_edges(self, dataset: str) -> List[Edge]:
        """

        Args:

        Returns:

        Raises:

        """
        return [item for item in chain(*[t.get_edges() for t in self.tables(dataset)]) if item is not None]

    @cache
    def nodes(self) -> List[BigqueryNode]:
        nodes = []
        for dataset in self.datasets:
            nodes.extend(self.get_nodes(dataset))
        return nodes

    @cache
    def edges(self) -> List[Edge]:
        edges = []
        for dataset in self.datasets:
            edges.extend(self.get_edges(dataset))
        return edges

    def get_nodes_and_edges(self) -> Tuple[List[BigqueryNode], List[Edge]]:
        """

        Args:

        Returns:

        Raises:

        """

        return self.nodes(), self.edges()


class LoggingConnector(BigqueryConnector):
    """ """

    def __init__(
        self,
        namespace: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[Union[str, List[str]]] = None,
        credentials: Optional[str] = None,
        window: Optional[int] = None,
    ):
        super().__init__(namespace, project, dataset, credentials)

        self.window = int(get_from_env("window", required=False, default=7)) if window is None else window
        self._logging_connection: Optional[logging.Client] = None

    def __enter__(self):
        super().__enter__()

        return self.logging_connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        super().__exit__(exc_type, exc_val, exc_tb)
        self.logging_close()

    def logging_connect(self) -> "LoggingConnector":
        """

        Args:

        Returns:

        Raises:

        """
        if self._logging_connection is None:
            credentials = None

            if self.credentials:
                json_acct_info = json.loads(self.credentials, strict=False)
                credentials = service_account.Credentials.from_service_account_info(json_acct_info)

            self._logging_connection = logging.Client(credentials=credentials, project=self.project)
        return self

    @property
    def logging_connection(self) -> logging.Client:
        """

        Args:

        Returns:

        Raises:

        """
        if self._logging_connection is None:
            raise Exception("Not connected, call `.connect()")
        return self._logging_connection

    def logging_close(self) -> None:
        """

        Args:

        Returns:

        Raises:

        """
        self.logging_connection.close()
        self._logging_connection = None

    @cached_property
    def logs(self) -> List[Any]:
        """Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.

        Args:

        Returns:

        Raises:

        """

        yesterday = datetime.now(timezone.utc) - timedelta(days=self.window)
        time_format = "%Y-%m-%dT%H:%M:%S.%f%z"

        filter_str = (
            'protoPayload.serviceName="bigquery.googleapis.com"'
            ' AND resource.type = "bigquery_project"'
            ' AND protoPayload.methodName="google.cloud.bigquery.v2.JobService.InsertJob"'
            f' AND timestamp>="{yesterday.strftime(time_format)}"'
        )

        datasets = [self.dataset] if isinstance(self.dataset, str) else self.dataset

        for dataset in datasets:
            filter_str += (
                f' AND NOT protoPayload.metadata.jobChange.job.jobStats.queryStats.referencedTables="projects/grai-demo/datasets/{dataset}/tables/INFORMATION_SCHEMA.TABLES"'
                f' AND NOT protoPayload.metadata.jobInsertion.job.jobStats.queryStats.referencedTables="projects/grai-demo/datasets/{dataset}/tables/INFORMATION_SCHEMA.TABLES"'
                f' AND NOT protoPayload.metadata.jobChange.job.jobStats.queryStats.referencedTables="projects/grai-demo/datasets/{dataset}/tables/INFORMATION_SCHEMA.COLUMNS"'
                f' AND NOT protoPayload.metadata.jobInsertion.job.jobStats.queryStats.referencedTables="projects/grai-demo/datasets/{dataset}/tables/INFORMATION_SCHEMA.COLUMNS"'
            )

        return self.logging_connection.list_entries(filter_=filter_str)

    def get_bigquery_edges(self, existing_nodes: List[BigqueryNode]) -> List[Edge]:
        """

        Args:

        Returns:

        Raises:

        """

        existing_node_unique_ids = {
            (node.name, node.table_schema) for node in existing_nodes if isinstance(node, Table)
        }

        def table_string_to_table_id(table_string: str) -> Optional[TableID]:
            table_string = table_string.split("/")

            schema = table_string[3]
            name = table_string[5]

            if (name, schema) not in existing_node_unique_ids:
                return None

            return TableID(
                table_schema=schema,
                name=name,
                namespace=self.namespace,
            )

        edges = set()

        for log in self.logs:
            content = log.to_api_repr()

            destination_table = (
                content.get("protoPayload", {})
                .get("metadata", {})
                .get("jobChange", {})
                .get("job", {})
                .get("jobConfig", {})
                .get("queryConfig", {})
                .get("destinationTable")
            ) or (
                content.get("protoPayload", {})
                .get("metadata", {})
                .get("jobInsertion", {})
                .get("job", {})
                .get("jobConfig", {})
                .get("queryConfig", {})
                .get("destinationTable")
            )

            if destination_table is None:
                continue

            destination = table_string_to_table_id(destination_table)

            if destination is None:
                continue

            referenced_tables = (
                content.get("protoPayload", {})
                .get("metadata", {})
                .get("jobChange", {})
                .get("job", {})
                .get("jobStats", {})
                .get("queryStats", {})
                .get("referencedTables", [])
            ) or (
                content.get("protoPayload", {})
                .get("metadata", {})
                .get("jobInsertion", {})
                .get("job", {})
                .get("jobStats", {})
                .get("queryStats", {})
                .get("referencedTables", [])
            )

            for table in referenced_tables:
                if destination_table == table:
                    continue

                source = table_string_to_table_id(table)

                if source is None:
                    continue

                edges.add(
                    Edge(
                        constraint_type=Constraint("bqm"),
                        source=source,
                        destination=destination,
                    )
                )

        return list(edges)

    def nodes(self) -> List[BigqueryNode]:
        return super().nodes()

    def edges(self) -> List[Edge]:
        edges = super().edges()
        bigquery_edges = self.get_bigquery_edges(self.nodes())

        return edges + bigquery_edges

    def get_nodes_and_edges(self) -> Tuple[List[BigqueryNode], List[Edge]]:
        return self.nodes(), self.edges()
