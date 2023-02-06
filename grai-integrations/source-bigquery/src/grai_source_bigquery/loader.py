import json
import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple

from google.cloud import bigquery
from google.oauth2 import service_account

from grai_source_bigquery.models import BigqueryNode, Column, Edge, Table


def get_from_env(
    label: str,
    default: Optional[Any] = None,
    required: bool = True,
    validator: Optional[Callable] = None,
):
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
    def __init__(
        self,
        namespace: Optional[str] = None,
        project: Optional[str] = None,
        dataset: Optional[str] = None,
        credentials: Optional[str] = None,
        **kwargs,
    ):
        self.namespace = get_from_env("namespace", "default") if namespace is None else namespace
        self.project = get_from_env("project", required=False) if project is None else project
        self.dataset = get_from_env("dataset", required=False) if dataset is None else dataset
        self.credentials = get_from_env("credentials", required=False) if credentials is None else credentials
        self._connection: Optional[bigquery.connector.BigqueryConnection] = None

        self._tables: Optional[List[Table]] = None
        self._foreign_keys: Optional[List[Edge]] = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self) -> "BigqueryConnector":
        if self._connection is None:
            credentials = None

            if self.credentials:
                json_acct_info = json.loads(self.credentials, strict=False)
                credentials = service_account.Credentials.from_service_account_info(json_acct_info)

            self._connection = bigquery.Client(credentials=credentials, project=self.project)
        return self

    @property
    def connection(self) -> bigquery.Client:
        if self._connection is None:
            raise Exception("Not connected, call `.connect()")
        return self._connection

    def close(self) -> None:
        self.connection.close()
        self._connection = None

    def query_runner(self, query: str, param_dict: Dict = {}) -> List[Dict]:
        return self.connection.query(query)

        # dict_cursor = self.connection.cursor(bigquery.connector.DictCursor)
        # dict_cursor.execute(query, param_dict)
        # return dict_cursor.fetchall()  # type: ignore

    def get_tables(self) -> List[Table]:
        """
        Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.
        """

        if self._tables is not None:
            return self._tables

        query = f"""
	        SELECT table_schema, table_name, table_type
            FROM {self.project}.{self.dataset}.INFORMATION_SCHEMA.TABLES
            WHERE table_schema != 'INFORMATION_SCHEMA'
            ORDER BY table_schema, table_name
        """

        res = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))

        additional_args = {
            "namespace": self.namespace,
            "table_dataset": self.dataset,
        }

        tables = [Table(**result, **additional_args) for result in res]
        for table in tables:
            table.columns = self.get_columns(table)

        self._tables = tables
        return self._tables

    def get_columns(self, table: Table) -> List[Column]:
        """
        Creates and returns a list of dictionaries for the specified
        schema.table in the database connected to.
        """

        query = f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM {self.project}.{self.dataset}.INFORMATION_SCHEMA.COLUMNS
            WHERE table_schema = '{table.table_schema}'
            AND table_name = '{table.name}'
        """

        res = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))

        addtl_args = {
            "namespace": table.namespace,
            "schema": table.table_schema,
            "table": table.name,
        }
        return [Column(**result, **addtl_args) for result in res]

    def get_nodes(self) -> List[BigqueryNode]:
        tables = self.get_tables()
        return list(chain(tables, *[t.columns for t in tables]))

    def get_edges(self) -> List[Edge]:
        tables = self.get_tables()
        edges = list(chain(*[t.get_edges() for t in tables]))
        return edges

    def get_nodes_and_edges(self) -> Tuple[List[BigqueryNode], List[Edge]]:
        nodes = self.get_nodes()
        edges = self.get_edges()
        return nodes, edges
