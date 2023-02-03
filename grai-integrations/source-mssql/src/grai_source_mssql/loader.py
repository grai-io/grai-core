import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union

import pyodbc
from pydantic import BaseSettings

from grai_source_mssql.models import Column, ColumnID, Edge, EdgeQuery, MysqlNode, Table


class MsSqlSettings:
    driver: str = "{SQL Server}"
    database: str
    server: str
    trusted_connection: Optional[bool] = None
    user: Optional[str]
    password: Optional[str]

    class Config:
        env_prefix = "GRAI_MSSQL_"

    def connection_string(self):
        connection_attributes = [f"DRIVER={self.driver}", f"Server={self.server}", f"DATABASE={self.database}"]
        if self.trusted_connection:
            connection_attributes.append("Trusted_Connection=yes")
        else:
            connection_attributes.extend([f"UID={self.user}", f"Pwd={self.password}"])
        return "; ".join(connection_attributes)


class MsSQLConnector:
    def __init__(
        self,
        driver: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        server: Optional[str] = None,
        namespace: Optional[str] = None,
    ):
        connection_values = {
            "driver": driver,
            "user": user,
            "password": password,
            "dbname": database,
            "server": server,
        }
        user_provided_connection_params = {k: v for k, v in connection_values.items() if v is not None}
        self.config = MsSqlSettings(**user_provided_connection_params)
        self.namespace = namespace
        self._connection = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        if self._connection is None:
            self._connection = pyodbc.connect(self.config.connection_string())

    @property
    def connection(self):
        if self._connection is None:
            raise Exception("Not connected, call `.connect()")
        return self._connection

    def close(self) -> None:
        self.connection.close()
        self._connection = None

    def query_runner(self, query: str, param_dict: Dict = {}) -> List[Dict]:
        cursor = self.connection.cursor()
        cursor.execute(query, param_dict)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def get_tables(self) -> List[Table]:
        """
        Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.
        """

        query = """
	        SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
            FROM sys.Tables
        """
        res = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))
        return [Table(**result, namespace=self.namespace) for result in res]

    def get_columns(self, table: Optional[Table] = None) -> List[Column]:
        """
        Creates and returns a list of dictionaries for the specified
        schema.table in the database connected to.
        """
        query = f"""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT, COLUMN_KEY, TABLE, TABLE_SCHEMA
            FROM INFORMATION_SCHEMA.COLUMNS
        """
        if table is not None:
            query = f"""
                {query}
                WHERE TABLE_SCHEMA = '{table.table_schema}'
                AND TABLE = '{table.name}'
            """

        res = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))

        addtl_args = {
            "namespace": self.namespace,
        }
        return [Column(**result, **addtl_args) for result in res]

    def get_foreign_keys(self) -> List[Edge]:
        """This needs to be tested / evaluated
        :param connection:
        :param table:
        :return:
        """

        query = """
            SELECT  obj.name AS FK_NAME,
                sch.name AS [schema_name],
                tab1.name AS [table],
                col1.name AS [column],
                tab2.name AS [referenced_table],
                col2.name AS [referenced_column]
            FROM sys.foreign_key_columns fkc
            INNER JOIN sys.objects obj
                ON obj.object_id = fkc.constraint_object_id
            INNER JOIN sys.tables tab1
                ON tab1.object_id = fkc.parent_object_id
            INNER JOIN sys.schemas sch
                ON tab1.schema_id = sch.schema_id
            INNER JOIN sys.columns col1
                ON col1.column_id = parent_column_id AND col1.object_id = tab1.object_id
            INNER JOIN sys.tables tab2
                ON tab2.object_id = fkc.referenced_object_id
            INNER JOIN sys.columns col2
                ON col2.column_id = referenced_column_id AND col2.object_id = tab2.object_id
        """
        addtl_args = {
            "namespace": self.namespace,
        }

        res = self.query_runner(query)

        # for item in res:
        #     item["self_columns"] = list(item["self_columns"].split(",")) if item["self_columns"] else []
        #     item["foreign_columns"] = list(item["foreign_columns"].split(",")) if item["foreign_columns"] else []

        res = ({k.lower(): v for k, v in result.items()} for result in res)

        filtered_results = (result for result in res if result["constraint_type"] == "f")

        return [EdgeQuery(**fk, **addtl_args).to_edge() for fk in filtered_results]

    def get_nodes(self) -> List[MysqlNode]:
        def get_nodes():
            for table in self.get_tables():
                table.columns = self.get_columns(table)
                yield [table]
                yield table.columns

        return list(chain(*get_nodes()))

    # TODO need to push edges between table -> columns

    def get_nodes_and_edges(self):
        tables = self.get_tables()
        column_idx = {(col.column_schema, col.table) for col in self.get_columns()}

        for table in tables:
            table.columns = column_idx[(table.table_schema, table.name)]

        nodes = list(chain(tables, *[t.columns for t in tables]))
        edges = list(chain(*[t.get_edges() for t in tables], self.get_foreign_keys()))

        return nodes, edges
