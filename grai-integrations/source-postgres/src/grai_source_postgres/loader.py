import os
from functools import cached_property
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple, Union

import psycopg2
import psycopg2.extras

from grai_source_postgres.models import (
    Column,
    ColumnID,
    Edge,
    EdgeQuery,
    PostgresNode,
    Table,
)


def get_from_env(label: str, default: Optional[Any] = None, validator: Callable = None):
    """

    Args:
        label (str):
        default (Optional[Any], optional):  (Default value = None)
        validator (Callable, optional):  (Default value = None)

    Returns:

    Raises:

    """
    env_key = f"GRAI_POSTGRES_{label.upper()}"
    result = os.getenv(env_key, default)
    if result is None:
        message = (
            f"Establishing postgres connection requires a {label}. "
            f"Either pass a value explicitly or set a {env_key} environment value."
        )
        raise Exception(message)
    return result if validator is None else validator(result)


class PostgresConnector:
    """ """

    def __init__(
        self,
        dbname: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        namespace: Optional[str] = None,
    ):
        self.host = host if host is not None else get_from_env("host", "localhost")
        self.port = port if port is not None else get_from_env("port", "5432", str)
        self.dbname = dbname if dbname is not None else get_from_env("dbname")
        self.user = user if user is not None else get_from_env("user")
        self.password = password if password is not None else get_from_env("password")
        self.namespace = namespace if namespace is not None else get_from_env("namespace", "default")

        # Combo allows the connection manager to guarantee the connector returns to it's previous connection
        # status after __exit__ is called.
        self._connection = None
        self._is_connected = False

    def __enter__(self):
        if not self._is_connected:
            self.connect()

        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if not self._is_connected:
            self.close()

    @property
    def connection_string(self) -> str:
        """

        Args:

        Returns:

        Raises:

        """
        return (
            f"dbname={self.dbname} host='{self.host}' user='{self.user}' password='{self.password}' port='{self.port}'"
        )

    def connect(self):
        """ """
        if self._connection is None:
            self._connection = psycopg2.connect(self.connection_string)
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

    def query_runner(self, query: str, param_dict: Dict = {}) -> List[Dict]:
        """

        Args:
            query (str):
            param_dict (Dict, optional):  (Default value = {})

        Returns:

        Raises:

        """
        cursor = self.connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        cursor.execute(query, param_dict)
        result = cursor.fetchall()
        return [dict(item) for item in result]

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
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_schema != 'pg_catalog'
            AND table_schema != 'information_schema'
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
            SELECT
                c.TABLE_SCHEMA AS "schema",
                c.TABLE_NAME AS "table",
                c.COLUMN_NAME,
                c.DATA_TYPE,
                c.IS_NULLABLE,
                c.COLUMN_DEFAULT,
                con.column_constraint
            FROM INFORMATION_SCHEMA.COLUMNS c
            LEFT JOIN (
                SELECT c.conname                                         AS constraint_name,
                       c.contype                                         AS column_constraint,
                       sch.nspname                                       AS "schema",
                       tbl.relname                                       AS "table",
                       col.attname                                       AS "column"
                FROM pg_constraint c
                       LEFT JOIN LATERAL UNNEST(c.conkey) WITH ORDINALITY AS u(attnum, attposition) ON TRUE
                       JOIN pg_class tbl ON tbl.oid = c.conrelid
                       JOIN pg_namespace sch ON sch.oid = tbl.relnamespace
                       LEFT JOIN pg_attribute col ON (col.attrelid = tbl.oid AND col.attnum = u.attnum)
                WHERE sch.nspname!='pg_catalog'
            ) con ON con.schema=c.table_schema
                  AND con.table=c.table_name
                  AND con.column=c.column_name
            WHERE c.table_schema not in ('pg_catalog', 'information_schema')
        """
        return [Column(**result, namespace=self.namespace) for result in self.query_runner(query)]

    def get_table_columns(self, table: Table) -> List[Column]:
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
        # query is from https://dba.stackexchange.com/questions/36979/retrieving-all-pk-and-fk/37068#37068
        # Only need constraint_types == 'f' for foreign keys but the others might be useful someday.
        query = """
            SELECT c.conname                                         AS constraint_name,
                   c.contype                                         AS constraint_type,
                   sch.nspname                                       AS "self_schema",
                   tbl.relname                                       AS "self_table",
                   ARRAY_AGG(col.attname ORDER BY u.attposition)     AS "self_columns",
                   f_sch.nspname                                     AS "foreign_schema",
                   f_tbl.relname                                     AS "foreign_table",
                   ARRAY_AGG(f_col.attname ORDER BY f_u.attposition) AS "foreign_columns",
                   pg_get_constraintdef(c.oid)                       AS definition
            FROM pg_constraint c
                   LEFT JOIN LATERAL UNNEST(c.conkey) WITH ORDINALITY AS u(attnum, attposition) ON TRUE
                   LEFT JOIN LATERAL UNNEST(c.confkey) WITH ORDINALITY AS f_u(attnum, attposition) ON f_u.attposition = u.attposition
                   JOIN pg_class tbl ON tbl.oid = c.conrelid
                   JOIN pg_namespace sch ON sch.oid = tbl.relnamespace
                   LEFT JOIN pg_attribute col ON (col.attrelid = tbl.oid AND col.attnum = u.attnum)
                   LEFT JOIN pg_class f_tbl ON f_tbl.oid = c.confrelid
                   LEFT JOIN pg_namespace f_sch ON f_sch.oid = f_tbl.relnamespace
                   LEFT JOIN pg_attribute f_col ON (f_col.attrelid = f_tbl.oid AND f_col.attnum = f_u.attnum)
            GROUP BY constraint_name, constraint_type, "self_schema", "self_table", definition, "foreign_schema", "foreign_table"
            ORDER BY "self_schema", "self_table";
        """
        addtl_args = {
            "namespace": self.namespace,
        }
        results = self.query_runner(query)
        filtered_results = (result for result in results if result["constraint_type"] == "f")
        result = (EdgeQuery(**fk, **addtl_args).to_edge() for fk in filtered_results)
        return [r for r in result if r is not None]

    def get_nodes(self) -> List[PostgresNode]:
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
        return [edge for edge in chain(*[t.get_edges() for t in self.tables], self.foreign_keys) if edge is not None]

    def get_nodes_and_edges(self) -> Tuple[List[PostgresNode], List[Edge]]:
        """

        Args:

        Returns:

        Raises:

        """
        nodes = self.get_nodes()
        edges = self.get_edges()

        return nodes, edges
