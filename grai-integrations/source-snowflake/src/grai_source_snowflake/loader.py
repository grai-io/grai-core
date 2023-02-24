import os
from functools import cached_property
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Tuple

import snowflake.connector

from grai_source_snowflake.models import (
    Column,
    ColumnID,
    Edge,
    EdgeQuery,
    SnowflakeNode,
    Table,
)


def string_is_quoted(string: str) -> bool:
    return string.startswith('"') and string.endswith('"')


def get_from_env(
    label: str,
    default: Optional[Any] = None,
    required: bool = True,
    validator: Optional[Callable] = None,
):
    env_key = f"GRAI_SNOWFLAKE_{label.upper()}"
    result = os.getenv(env_key, default)
    if result is None and required:
        message = (
            f"Establishing snowflake connection requires a {label}. "
            f"Either pass a value explicitly or set a {env_key} environment value."
        )
        raise Exception(message)
    return result if validator is None else validator(result)


class SnowflakeConnector:
    def __init__(
        self,
        account: Optional[str] = None,
        user: Optional[str] = None,
        password: Optional[str] = None,
        warehouse: Optional[str] = None,
        role: Optional[str] = None,
        database: Optional[str] = None,
        schema: Optional[str] = None,
        namespace: Optional[str] = None,
        **kwargs,
    ):
        self.account = get_from_env("account") if account is None else account
        self.user = get_from_env("user") if user is None else user
        self.password = get_from_env("password") if password is None else password
        self.warehouse = get_from_env("warehouse") if warehouse is None else warehouse
        self.role = get_from_env("role", required=False) if role is None else role
        self.database = get_from_env("database", required=False) if database is None else database
        self.schema = get_from_env("schema", required=False) if schema is None else schema
        self.namespace = get_from_env("namespace", "default") if namespace is None else namespace
        self.additional_conn_kwargs = kwargs
        self._connection: Optional[snowflake.connector.SnowflakeConnection] = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection_dict(self) -> Dict[str, str]:
        connection_keys = [
            "account",
            "user",
            "password",
            "warehouse",
            "role",
            "database",
            "schema",
        ]
        return {key: value for key in connection_keys if (value := getattr(self, key)) is not None}

    def connect(self) -> "SnowflakeConnector":
        if self._connection is None:
            self._connection = snowflake.connector.connect(**self.connection_dict, **self.additional_conn_kwargs)
        return self

    @property
    def connection(self) -> snowflake.connector.SnowflakeConnection:
        if self._connection is None:
            raise Exception("Not connected, call `.connect()")
        return self._connection

    def close(self) -> None:
        self.connection.close()
        self._connection = None

    def query_runner(self, query: str, param_dict: Dict = {}) -> List[Dict]:
        dict_cursor = self.connection.cursor(snowflake.connector.DictCursor)
        dict_cursor.execute(query, param_dict)
        return dict_cursor.fetchall()  # type: ignore

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
            WHERE table_schema != 'INFORMATION_SCHEMA'
            ORDER BY table_schema, table_name
        """
        res = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))

        additional_args = {
            "namespace": self.namespace,
            "table_database": self.connection_dict["database"],
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

        def quoted_table_name(table_name: str) -> str:
            return table_name if table_name.startswith('"') and table_name.endswith('"') else f"'{table_name.upper()}'"

        query = f"""
            SELECT column_name, data_type, is_nullable, column_default, table_schema, table_name
            FROM information_schema.columns
            WHERE table_schema != 'INFORMATION_SCHEMA'
        """

        res = [{k.lower(): v for k, v in result.items()} for result in self.query_runner(query)]
        for item in res:
            item.update(
                {
                    "table": item["table_name"],
                    #'table': quoted_table_name(item['table_name']),
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

        schema = table_id[0] if string_is_quoted(table_id[0]) else table_id[0].upper()
        name = table_id[1] if string_is_quoted(table_id[1]) else table_id[1].upper()
        table_id = (schema, name)
        if table_id in self.column_map:
            return self.column_map[table_id]
        else:
            raise Exception(f"No columns found for table with schema={schema} and name={name}")

    @cached_property
    def foreign_keys(self) -> List[Edge]:
        """This needs to be tested / evaluated
        :param connection:
        :param table:
        :return:
        """
        # This query only returns foreign keys, there is also exported keys and primary keys.
        # Information schema itself doesn't carry the column for foreign keys
        # show IMPORTED KEYS in database '{self.connection_dict['database']}'

        query = f"""
        show IMPORTED KEYS
        """
        addtl_args = {
            "namespace": self.namespace,
        }

        imported_keys = self.query_runner(query)

        key_rename_map = {
            "constraint_name": "fk_name",
            "self_database": "pk_database_name",
            "self_schema": "pk_schema_name",
            "self_table": "pk_table_name",
            "self_columns": "pk_column_name",
            "foreign_database": "fk_database_name",
            "foreign_schema": "fk_schema_name",
            "foreign_table": "fk_table_name",
            "foreign_columns": "fk_column_name",
        }
        for item in imported_keys:
            item |= {k: item.pop(v) for k, v in key_rename_map.items()}
            item["constraint_type"] = "f"
            item["definition"] = ""  # Available on another table
            item["self_columns"] = item["self_columns"].split(",")
            item["foreign_columns"] = item["foreign_columns"].split(",")

        res = ({k.lower(): v for k, v in result.items()} for result in imported_keys)
        fks = [EdgeQuery(**fk, **addtl_args).to_edge() for fk in res]

        return fks

    def get_nodes(self) -> List[SnowflakeNode]:
        # return list(chain(self.tables, *[t.columns for t in self.tables]))
        return list(chain(self.tables, self.columns))

    def get_edges(self) -> List[Edge]:
        edges = list(chain(*[t.get_edges() for t in self.tables], self.foreign_keys))
        return edges

    def get_nodes_and_edges(self) -> Tuple[List[SnowflakeNode], List[Edge]]:
        nodes = self.get_nodes()
        edges = self.get_edges()
        return nodes, edges
