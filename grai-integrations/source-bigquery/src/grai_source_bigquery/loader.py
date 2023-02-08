import json
import os
from functools import cached_property
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

    @cached_property
    def tables(self) -> List[Table]:
        """
        Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.
        """
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
            table.columns = self.get_table_columns(table)
        return tables

    @cached_property
    def columns(self) -> List[Column]:
        """
        Creates and returns a list of dictionaries for the specified
        schema.table in the database connected to.
        """

        query = f"""
            SELECT column_name, data_type, is_nullable, column_default, table_schema, table_name
            FROM {self.project}.{self.dataset}.INFORMATION_SCHEMA.COLUMNS
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

    @cached_property
    def column_map(self):
        result_map = {}
        for col in self.columns:
            table_id = (col.column_schema, col.table)
            result_map.setdefault(table_id, [])
            result_map[table_id].append(col)
        return result_map

    def get_table_columns(self, table: Table):
        table_id = (table.table_schema, table.name)
        if table_id in self.column_map:
            return self.column_map[table_id]

        schema = table_id[0]
        name = table_id[1]
        table_id = (schema, name)
        if table_id in self.column_map:
            return self.column_map[table_id]
        else:
            raise Exception(f"No columns found for table with schema={schema} and name={name}")

    def get_nodes(self) -> List[BigqueryNode]:
        return list(chain(self.tables, self.columns))

    def get_edges(self) -> List[Edge]:
        return list(chain(*[t.get_edges() for t in self.tables]))

    def get_nodes_and_edges(self) -> Tuple[List[BigqueryNode], List[Edge]]:
        nodes = self.get_nodes()
        edges = self.get_edges()
        return nodes, edges
