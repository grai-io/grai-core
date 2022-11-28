import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union
import snowflake.connector
from grai_source_snowflake.models import (
    Column,
    ColumnID,
    Edge,
    EdgeQuery,
    snowflakeNode,
    Table,
)


def get_from_env(label: str, default: Optional[Any] = None, validator: Callable = None):
    env_key = f"GRAI_SNOWFLAKE_{label.upper()}"
    result = os.getenv(env_key, default)
    if result is None:
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
    ):
        self.account = account 
        self.user = user
        self.password = password
        self.warehouse = warehouse
        self.role = role
        self.database = database
        self.schema = schema

        self.namespace = (
            namespace if namespace is not None else get_from_env("namespace", "default")
        )
        self._connection = None

    def __enter__(self):
        return self.connect()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()

    @property
    def connection_dict(self) -> dict:
        return {'account': self.account,'user': self.user, 'password': self.password, 'warehouse': self.warehouse, 'role': self.role, 'database': self.database, 'schema': self.schema}

    def connect(self):
        if self._connection is None:
            self._connection = snowflake.connector.connect(**self.connection_dict)
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
        dict_cursor = self.connection.cursor(snowflake.connector.DictCursor)
        dict_cursor.execute(query, param_dict)
        result = dict_cursor.fetchall()
        #return [dict(item) for item in result]
        return result

    def get_tables(self) -> List[Table]:
        """
        Create and return a list of dictionaries with the
        schemas and names of tables in the database
        connected to by the connection argument.
        """

        query = """
	        SELECT table_schema, table_name
            FROM information_schema.tables
            WHERE table_schema != 'INFORMATION_SCHEMA'
            and table_type = 'BASE TABLE'
            ORDER BY table_schema, table_name
        """
        res = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))

        addtl_args = {
            "namespace": self.namespace,
            "table_database": self.connection_dict['database']
        }

        return [Table(**result, **addtl_args) for result in res]

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
        """

        res = ({k.lower(): v for k, v in result.items()} for result in self.query_runner(query))

        addtl_args = {
            "namespace": table.namespace,
            "schema": table.table_schema,
            "table": table.name,
        }
        return [Column(**result, **addtl_args) for result in res]

    def get_foreign_keys(self) -> List[Edge]:
        """This needs to be tested / evaluated
        :param connection:
        :param table:
        :return:
        """
        # This query only returns foreign keys, there is also exported keys and primary keys. Information schema itself doesn't carry the column for foreign keys
        query = """
        show IMPORTED KEYS
        """
        addtl_args = {
            "namespace": self.namespace,
        }

        res = self.query_runner(query)

        for i in res:
            i["constraint_name"] = i.pop("fk_name")
            i["constraint_type"] = 'f'
            i["definition"] = '' #Available on another table
            i["self_database"] = i.pop("pk_database_name")
            i["self_schema"] = i.pop("pk_schema_name")
            i["self_table"] = i.pop("pk_table_name")
            i["self_columns"] = i.pop("pk_column_name")
            i["self_columns"] = list(i["self_columns"].split(","))

            i["foreign_database"] = i.pop("fk_database_name")
            i["foreign_schema"] = i.pop("fk_schema_name")
            i["foreign_table"] = i.pop("fk_table_name")
            i["foreign_columns"] = i.pop("fk_column_name")
            i["foreign_columns"] = list(i["foreign_columns"].split(","))

        res = ({k.lower(): v for k, v in result.items()} for result in res)

        return [EdgeQuery(**fk, **addtl_args).to_edge() for fk in res]

    def get_nodes(self) -> List[snowflakeNode]:
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
