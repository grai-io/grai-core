import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union

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
        self.namespace = (
            namespace if namespace is not None else get_from_env("namespace", "default")
        )
        self._connection = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection_string(self) -> str:
        return f"dbname={self.dbname} host='{self.host}' user='{self.user}' password='{self.password}' port='{self.port}'"

    def connect(self):
        if self._connection is None:
            self._connection = psycopg2.connect(self.connection_string)
        return self

    @property
    def connection(self):
        if self._connection is None:
            raise Exception("Not connected, call `.connect()")
        return self._connection

    def close(self) -> None:
        self.connection.close()
        self._connection = None

    def query_runner(self, query: str, param_dict: Dict = {}) -> List[Dict]:
        with self.connection.cursor(
            cursor_factory=psycopg2.extras.RealDictCursor
        ) as cursor:
            cursor.execute(query, param_dict)
            result = cursor.fetchall()
        return [dict(item) for item in result]

    def get_tables(self) -> List[Table]:
        """
        Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.
        """

        query = """
            SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema != 'pg_catalog'
            AND table_schema != 'information_schema'
            AND table_type='BASE TABLE'
            ORDER BY table_schema, table_name
        """
        return [
            Table(**result, namespace=self.namespace)
            for result in self.query_runner(query)
        ]

    def get_columns(self, table: Table) -> List[Column]:
        """
        Creates and returns a list of dictionaries for the specified
        schema.table in the database connected to.
        """

        query = f"""
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = '{table.table_schema}'
            AND table_name = '{table.name}'
            ORDER BY ordinal_position
        """
        addtl_args = {
            "namespace": table.namespace,
            "schema": table.table_schema,
            "table": table.name,
        }
        return [Column(**result, **addtl_args) for result in self.query_runner(query)]

    def get_foreign_keys(self) -> List[Edge]:
        """This needs to be tested / evaluated
        :param connection:
        :param table:
        :return:
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
        filtered_results = (
            result for result in results if result["constraint_type"] == "f"
        )
        return [EdgeQuery(**fk, **addtl_args).to_edge() for fk in filtered_results]

    def get_nodes(self) -> List[PostgresNode]:
        def get_nodes():
            for table in self.get_tables():
                table.columns = self.get_columns(table)
                yield [table]
                yield table.columns

        return list(chain(*get_nodes()))

    # TODO need to push edges between table -> columns

    def get_nodes_and_edges(self):
        tables = self.get_tables()
        edges = []
        for table in tables:
            table.columns = self.get_columns(table)

        edges = list(chain(*[t.get_edges() for t in tables], self.get_foreign_keys()))

        nodes = list(chain(tables, *[t.columns for t in tables]))
        return nodes, edges
