import os
from functools import cached_property
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import redshift_connector
from pydantic import BaseSettings, SecretStr, validator
from redshift_connector.core import Connection

from grai_source_redshift.models import (
    Column,
    ColumnID,
    Edge,
    EdgeQuery,
    LateBindingViewColumn,
    RedshiftNode,
    Table,
)


class RedshiftConfig(BaseSettings):
    """ """

    user: Optional[str] = None
    password: Optional[SecretStr] = None
    database: Optional[str] = None
    host: Optional[str] = None
    port: Optional[int] = None

    class Config:
        """ """

        env_prefix = "grai_redshift_"
        env_file = ".env"


class RedshiftConnector:
    """ """

    def __init__(
        self,
        namespace: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        **kwargs,
    ):
        passthrough_kwargs = {
            "user": user,
            "password": password,
            "database": database,
            "host": host,
            "port": port,
        }

        self.namespace = namespace
        self.config = RedshiftConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})
        self.redshift_params: Dict[str, Any] = kwargs
        self._connection: Optional[Connection] = None
        self._is_connected: Optional[bool] = None

    def __enter__(self):
        if not self._is_connected:
            self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._is_connected:
            self.close()

    def connect(self):
        """ """
        conn_params = {k: v for k, v in self.config.dict().items() if v is not None}
        if "password" in conn_params:
            conn_params["password"] = conn_params["password"].get_secret_value()

        if self._connection is None:
            self._connection = redshift_connector.connect(**conn_params, **self.redshift_params)
            self._is_connected = True
        return self

    @property
    def connection(self):
        """ """
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
        self._is_connected = False

    def query_runner(self, query: str) -> List[Dict]:
        """

        Args:
            query (str):

        Returns:

        Raises:

        """
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, item)) for item in cursor.fetchall()]

    @cached_property
    def tables(self) -> List[Table]:
        """Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.

        Args:

        Returns:

        Raises:

        """

        query = """
            SELECT table_catalog, table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_internal')
            ORDER BY table_schema, table_name
        """

        tables = [Table(**result, namespace=self.namespace) for result in self.query_runner(query)]
        for table in tables:
            table.columns = self.get_table_columns(table)
        return tables

    @cached_property
    def columns(self) -> List[Column]:
        """Creates and returns a list of dictionaries for the specified
        schema.table in the database connected to.

        Args:

        Returns:

        Raises:

        """
        query = f"""
            SELECT table_catalog,
                   table_schema AS column_schema,
                   table_name,
                   column_name,
                   column_default,
                   is_nullable,
                   data_type,
                   character_maximum_length,
                   numeric_precision
            FROM information_schema.columns
            WHERE table_schema NOT IN ('pg_catalog', 'information_schema', 'pg_internal')
            ORDER BY ordinal_position;
        """
        columns = [Column(**result, namespace=self.namespace) for result in self.query_runner(query)]

        late_binding_query = """
            select *
            from pg_get_late_binding_view_cols()
            cols(column_schema name, table_name name, column_name name, data_type varchar, col_num int);
        """

        late_binding_views = [
            LateBindingViewColumn(**result, namespace=self.namespace)
            for result in self.query_runner(late_binding_query)
        ]
        columns.extend(late_binding_views)
        return columns

    def get_table_columns(self, table: Table):
        """

        Args:
            table (Table):

        Returns:

        Raises:

        """
        table_id = (table.table_schema, table.name)
        if table_id in self.column_map:
            return self.column_map[table_id]
        else:
            raise Exception(f"No columns found for table with schema={table.table_schema} and name={table.name}")

    @cached_property
    def column_map(self) -> Dict[Tuple[str, str], List[Column]]:
        """

        Args:

        Returns:

        Raises:

        """
        result_map: Dict[Tuple[str, str], List[Column]] = {}
        for col in self.columns:
            table_id = (col.column_schema, col.table)
            result_map.setdefault(table_id, [])
            result_map[table_id].append(col)
        return result_map

    @cached_property
    def foreign_keys(self) -> List[Edge]:
        """This needs to be tested / evaluated

        Args:

        Returns:

        Raises:

        """
        # query is from https://alberton.info/postgresql_meta_info.html
        # detailed constraint info section
        query = """
            SELECT tc.constraint_name,
                   tc.constraint_type,
                   tc.table_catalog AS self_catalog,
                   tc.table_schema AS self_schema,
                   tc.table_name AS self_table,
                   kcu.column_name AS self_column,
                   ccu.table_catalog AS foreign_catalog,
                   ccu.table_schema AS foreign_schema,
                   ccu.table_name AS foreign_table,
                   ccu.column_name AS foreign_column
                 FROM information_schema.table_constraints tc
            LEFT JOIN information_schema.key_column_usage kcu
                   ON tc.constraint_catalog = kcu.constraint_catalog
                  AND tc.constraint_schema = kcu.constraint_schema
                  AND tc.constraint_name = kcu.constraint_name
            LEFT JOIN information_schema.referential_constraints rc
                   ON tc.constraint_catalog = rc.constraint_catalog
                  AND tc.constraint_schema = rc.constraint_schema
                  AND tc.constraint_name = rc.constraint_name
            LEFT JOIN information_schema.constraint_column_usage ccu
                   ON rc.unique_constraint_catalog = ccu.constraint_catalog
                  AND rc.unique_constraint_schema = ccu.constraint_schema
                  AND rc.unique_constraint_name = ccu.constraint_name
        """
        addtl_args = {"namespace": self.namespace}
        results = self.query_runner(query)
        filtered_results = (result for result in results if result["constraint_type"] == "FOREIGN KEY")
        result = [EdgeQuery(**fk, **addtl_args).to_edge() for fk in filtered_results]
        return [r for r in result if r is not None]

    def get_nodes(self) -> List[RedshiftNode]:
        """

        Args:

        Returns:

        Raises:

        """
        return list(chain(self.tables, self.columns))

    def get_edges(self) -> List[Edge]:
        """

        Args:

        Returns:

        Raises:

        """
        return list(chain(*[t.get_edges() for t in self.tables], self.foreign_keys))

    def get_nodes_and_edges(self) -> Tuple[List[RedshiftNode], List[Edge]]:
        """

        Args:

        Returns:

        Raises:

        """
        nodes = self.get_nodes()
        edges = self.get_edges()

        return nodes, edges
