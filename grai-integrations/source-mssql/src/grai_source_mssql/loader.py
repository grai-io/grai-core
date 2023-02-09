import os
import warnings
from enum import Enum
from functools import cached_property
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union

import pydantic
import pyodbc
from pydantic import SecretStr, root_validator, validator

from grai_source_mssql.models import Column, ColumnID, Edge, EdgeQuery, MsSqlNode, Table

ENV_PREFIX = "GRAI_MSSQL_"


class BaseSettings(pydantic.BaseSettings):
    class Config:
        env_prefix = ENV_PREFIX


class Protocol(Enum):
    TCP = "tcp"
    ICP = "Icp"
    NP = "NP"


class MsSqlSettings(BaseSettings):
    driver: Optional[str] = None
    database: Optional[str] = None
    server: Optional[str] = None
    protocol: Optional[Protocol] = None
    host: Optional[str] = None
    port: Optional[str] = None
    trusted_connection: Optional[bool] = None
    trust_server_certificate: Optional[bool] = None
    user: Optional[str]
    password: Optional[SecretStr]
    encrypt: Optional[bool]
    additional_connection_strings: Optional[List[str]] = None

    @validator("protocol")
    def validate_protocol(cls, value):
        if value is None:
            return Protocol.TCP

        return Protocol(value)

    def connection_string(self):
        connection_attributes = [f"DRIVER={self.driver}"]
        if self.trusted_connection:
            connection_attributes.append("Trusted_Connection=yes")
        else:
            connection_attributes.extend([f"UID={self.user}", f"Pwd={self.password.get_secret_value()}"])
        if self.encrypt is not None:
            connection_attributes.append(f"Encrypt={'yes' if self.encrypt else 'no'}")
        if self.database is not None:
            connection_attributes.append(f"DATABASE={self.database}")

        if self.server is not None:
            connection_attributes.append(f"Server={self.server}")
        elif self.host is not None:
            protocol_string = "" if self.protocol is None else f"{self.protocol.value}:"
            port_string = "" if self.port is None else f",{self.port}"
            server_string = f"Server={protocol_string}{self.host}{port_string}"
            connection_attributes.append(server_string)
        else:
            raise Exception("Connection strings require either `server` or a `host`/`port` combination.")

        if self.trust_server_certificate is not None:
            connection_attributes.append(f"TrustServerCertificate={'yes' if self.trust_server_certificate else 'no'}")
        if self.additional_connection_strings is not None:
            connection_attributes.extend(self.additional_connection_strings)

        return "; ".join(connection_attributes)

    @validator("driver")
    def validate_driver(cls, value):
        available_drivers = pyodbc.drivers()
        if value is None:
            message = f"Running the MS Server connector requires either a `driver` parameter or {ENV_PREFIX}DRIVER environment variable. Normally we would attempt to detect an available driver installed on your system, however, in this case none were found. "
            assert len(available_drivers) >= 1, message
            return available_drivers[0]
        elif value not in available_drivers:
            warnings.warn(
                f"Specified driver {value} not found in the list of available pyodbc drivers {available_drivers}"
            )
        return value

    @root_validator(pre=True)
    def parse_empty_values(cls, values):
        """Empty strings should be treated as missing"""
        new_values = values.copy()
        for k, v in values.items():
            if v == "":
                new_values.pop(k)
        return new_values


class MsSqlGraiSettings(BaseSettings):
    namespace: str = "default"


class ConnectorSettings(MsSqlSettings, MsSqlGraiSettings):
    pass


class MsSQLConnector:
    def __init__(
        self,
        driver: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        database: Optional[str] = None,
        server: Optional[str] = None,
        protocol: Optional[str] = None,
        host: Optional[str] = None,
        port: Optional[str] = None,
        encrypt: Optional[bool] = None,
        namespace: Optional[str] = None,
        additional_connection_strings: Optional[List[str]] = None,
    ):
        connection_values = {
            "driver": driver,
            "user": user,
            "password": password,
            "database": database,
            "server": server,
            "protocol": protocol,
            "host": host,
            "port": port,
            "encrypt": encrypt,
            "namespace": namespace,
            "additional_connection_strings": additional_connection_strings,
        }
        user_provided_connection_params = {k: v for k, v in connection_values.items() if v is not None}
        self.config = ConnectorSettings(**user_provided_connection_params)
        self._connection = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    def connect(self):
        if self._connection is None:
            self._connection = pyodbc.connect(self.config.connection_string())
        return self

    @property
    def connection(self):
        if self._connection is None:
            raise Exception("Not connected, call `.connect()")
        return self._connection

    def close(self) -> None:
        self.connection.close()
        self._connection = None

    def query_runner(self, query: str, params: List = []) -> List[Dict]:
        cursor = self.connection.cursor()
        # queries must be parameterized with ?
        # https://github.com/mkleehammer/pyodbc/wiki/Getting-started#parameters
        cursor.execute(query, *params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    @cached_property
    def tables(self) -> List[Table]:
        """
        Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.
        """

        query = """
	        SELECT TABLE_SCHEMA, TABLE_NAME, TABLE_TYPE
            FROM INFORMATION_SCHEMA.TABLES
        """
        tables = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))
        tables = [Table(**result, namespace=self.config.namespace) for result in tables]
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
            SELECT c.COLUMN_NAME,
                   c.DATA_TYPE,
                   c.IS_NULLABLE,
                   c.COLUMN_DEFAULT,
                   c.TABLE_NAME,
                   c.TABLE_SCHEMA,
                   tc.CONSTRAINT_TYPE AS [column_constraint]
            FROM INFORMATION_SCHEMA.COLUMNS c
            LEFT JOIN INFORMATION_SCHEMA.CONSTRAINT_COLUMN_USAGE cu
                ON c.TABLE_NAME = cu.TABLE_NAME
                AND c.TABLE_SCHEMA = cu.TABLE_SCHEMA
                AND c.COLUMN_NAME = cu.COLUMN_NAME
            LEFT JOIN INFORMATION_SCHEMA.TABLE_CONSTRAINTS tc
                ON cu.CONSTRAINT_NAME = tc.CONSTRAINT_NAME
        """
        res = [{k.lower(): v for k, v in result.items()} for result in self.query_runner(query)]
        for item in res:
            item.update(
                {
                    "table": item["table_name"],
                    "column_schema": item["table_schema"],
                }
            )

        result = [Column(**result, namespace=self.config.namespace) for result in res]
        return result

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
        else:
            raise Exception(f"No columns found for table with schema={table.table_schema} and name={table.name}")

    @cached_property
    def foreign_keys(self) -> List[Edge]:
        """This needs to be tested / evaluated
        :param connection:
        :param table:
        :return:
        """

        query = """
            SELECT sch.name AS [self_schema],
                tab1.name AS [self_table],
                col1.name AS [self_columns],
                tab2.name AS [foreign_table],
                col2.name AS [foreign_columns]
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
        res = self.query_runner(query)

        res = [{k.lower(): v for k, v in result.items()} for result in res]
        for item in res:
            item.update(
                {
                    "constraint_type": "f",
                    "definition": "",
                    "foreign_schema": item["self_schema"],  # TODO: This is not necessarily true
                    "namespace": self.config.namespace,
                    "constraint_name": "",
                    "self_columns": list(item["self_columns"].split(",")),
                    "foreign_columns": list(item["foreign_columns"].split(",")),
                }
            )
        return [EdgeQuery(**fk).to_edge() for fk in res]

    def get_nodes(self) -> List[MsSqlNode]:
        return list(chain(self.tables, self.columns))

    def get_edges(self):
        return list(chain(*[t.get_edges() for t in self.tables], self.foreign_keys))

    def get_nodes_and_edges(self):
        nodes = self.get_nodes()
        edges = self.get_edges()

        return nodes, edges
