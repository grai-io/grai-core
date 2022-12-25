import os
from itertools import chain
from typing import Any, Callable, Dict, List, Optional, Union, Iterable
import requests
from functools import partial
import string
import random

from grai_source_fivetran.models import (
    Column,
    ColumnID,
    Edge,
    EdgeQuery,
    PostgresNode,
    Table,
    TableResult,
    ColumnResult,
    SchemaResult
)


def get_from_env(label: str, default: Optional[Any] = None, validator: Callable = None):
    package = "FIVETRAN"
    env_key = f"GRAI_{package}_{label.upper()}"
    result = os.getenv(env_key, default)
    if result is None:
        message = (
            f"Establishing {package} connection requires a {label}. "
            f"Either pass a value explicitly or set a {env_key} environment value."
        )
        raise Exception(message)
    return result if validator is None else validator(result)


class FivetranConnector:
    def __init__(
        self,
        connector_id: str,
        user: Optional[str] = None,
        password: Optional[str] = None,
        fivetran_endpoint: str = "https://api.fivetran.com/v1/"
    ):
        self.connector_id = connector_id
        self.base_endpoint = fivetran_endpoint
        self.user = user if user is not None else get_from_env("user")
        self.password = password if password is not None else get_from_env("password")

        self._connection = None

    @property
    def auth(self):
        return self.user, self.password

    @property
    def get(self) -> Callable[..., requests.Response]:
        return partial(requests.get, auth=self.auth)

    @property
    def post(self) -> Callable[..., requests.Response]:
        return partial(requests.post, auth=self.auth)

    @property
    def patch(self) -> Callable[..., requests.Response]:
        return partial(requests.patch, auth=self.auth)

    @property
    def delete(self) -> Callable[..., requests.Response]:
        return partial(requests.delete, auth=self.auth)

    @property
    def metadata_endpoint(self) -> str:
        return f"{self.base_endpoint}metadata/connectors/{self.connector_id}/"

    @staticmethod
    def get_cursor() -> str:
        return ''.join(random.choices(string.ascii_lowercase, k=10))

    @staticmethod
    def make_request(request: Callable[..., requests.Response], url: str, headers: Dict, params: Dict, **kwargs) -> Dict:
        result = request(url, headers=headers, params=params, **kwargs)
        assert result.status_code == 200
        return result.json()

    def paginated_query(self, request, url, headers={}, params={}, **kwargs) -> Iterable[Dict]:
        result = self.make_request(request, url, headers=headers, params=params, **kwargs)
        yield result

        while 'nextCursor' in result['data']:
            params['cursor'] = result['data']['nextCursor']
            result = self.make_request(request, url, headers=headers, params=params, **kwargs)
            yield result

    def get_tables(self, limit=100):
        url = f"{self.metadata_endpoint}tables"
        headers = {"Accept": "application/json"}
        query = {
            "cursor": self.get_cursor(),
            "limit": limit
        }

        table_results = []
        for page in self.paginated_query(self.get, url, headers, query):
            new_table_results = [TableResult(**table) for table in page['data']['items']]
            table_results.extend(new_table_results)
        return table_results

    def get_columns(self, limit=100):
        url = f"{self.metadata_endpoint}columns"
        headers = {"Accept": "application/json"}
        query = {
            "cursor": self.get_cursor(),
            "limit": limit
        }

        column_results = []
        for page in self.paginated_query(self.get, url, headers, query):
            new_column_results = [ColumnResult(**table) for table in page['data']['items']]
            column_results.extend(new_column_results)
        return column_results

    def get_schemas(self, limit=100):
        url = f"{self.metadata_endpoint}schemas"
        headers = {"Accept": "application/json"}
        query = {
            "cursor": self.get_cursor(),
            "limit": limit
        }

        schema_results = []
        for page in self.paginated_query(self.get, url, headers, query):
            new_schema_results = [SchemaResult(**table) for table in page['data']['items']]
            schema_results.extend(new_schema_results)
        return schema_results

