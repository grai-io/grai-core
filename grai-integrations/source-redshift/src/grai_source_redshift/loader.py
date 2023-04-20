import os
from functools import cached_property
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union

import redshift_connector
from pydantic import BaseSettings, SecretStr, validator
from redshift_connector.core import Connection

from grai_source_redshift.models import (
    Column,
    ColumnID,
    Edge,
    EdgeQuery,
    RedshiftNode,
    Table,
)


class RedshiftConfig(BaseSettings):
    user: Optional[str] = (None,)
    password: Optional[SecretStr] = (None,)
    database: Optional[str] = (None,)
    host: Optional[str] = (None,)
    port: Optional[int] = (5439,)
    namespace: Optional[str] = None

    @validator("endpoint")
    def validate_endpoint(cls, value):
        return value.rstrip("/")

    class Config:
        env_prefix = "grai_redshift_"
        env_file = ".env"


class RedshiftConnector:
    def __init__(
        self,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[Union[str, int]] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ):
        passthrough_kwargs = {
            "user": user,
            "password": password,
            "database": database,
            "host": host,
            "port": port,
            "namespace": namespace,
        }
        self.config = RedshiftConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})
        self.redshift_params: [Dict[str, Any]] = kwargs
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
        if self._connection is None:
            self._connection = redshift_connector.connect(
                host=self.config.host,
                port=self.config.port,
                database=self.config.database,
                user=self.config.user,
                password=self.config.password.get_secret_value(),
                **self.redshift_params,
            )
            self._is_connected = True
        return self

    @property
    def connection(self):
        if self._connection is None:
            raise Exception("Not connected, call `.connect()")
        return self._connection

    def close(self) -> None:
        self.connection.close()
        self._connection = None
        self._is_connected = False

    def query_runner(self, query: str) -> List[Dict]:
        cursor = self.connection.cursor()
        cursor.execute(query)
        columns = [column[0] for column in cursor.description]
        return [dict(zip(columns, item)) for item in cursor.fetchall()]

    @cached_property
    def tables(self) -> List[Table]:
        """
        Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.
        """

        query = """
            SELECT table_schema, table_name, table_type
            FROM information_schema.tables
            WHERE table_schema != 'pg_catalog'
            AND table_schema != 'information_schema'
            ORDER BY table_schema, table_name
        """
        tables = [Table(**result, namespace=self.config.namespace) for result in self.query_runner(query)]
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
        return [Column(**result, namespace=self.config.namespace) for result in self.query_runner(query)]

    def get_table_columns(self, table: Table):
        table_id = (table.table_schema, table.name)
        if table_id in self.column_map:
            return self.column_map[table_id]
        else:
            raise Exception(f"No columns found for table with schema={table.table_schema} and name={table.name}")

    @cached_property
    def column_map(self):
        result_map = {}
        for col in self.columns:
            table_id = (col.column_schema, col.table)
            result_map.setdefault(table_id, [])
            result_map[table_id].append(col)
        return result_map

    @cached_property
    def foreign_keys(self) -> List[Edge]:
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
            "namespace": self.config.namespace,
        }
        results = self.query_runner(query)
        filtered_results = (result for result in results if result["constraint_type"] == "f")
        return [EdgeQuery(**fk, **addtl_args).to_edge() for fk in filtered_results]

    def get_nodes(self) -> List[RedshiftNode]:
        return list(chain(self.tables, self.columns))

    def get_edges(self):
        return list(chain(*[t.get_edges() for t in self.tables], self.foreign_keys))

    def get_nodes_and_edges(self):
        nodes = self.get_nodes()
        edges = self.get_edges()

        return nodes, edges
