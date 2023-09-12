import asyncio
from functools import cached_property
from itertools import chain
from typing import Callable, Dict, List, Optional, Tuple, TypedDict, Union

import httpx
import requests
from pydantic import (
    AnyHttpUrl,
    BaseModel,
    BaseSettings,
    Json,
    SecretStr,
    parse_obj_as,
    validator,
)
from requests.exceptions import ConnectionError
from retrying import retry

from grai_source_metabase import api
from grai_source_metabase.models import (
    Collection,
    Edge,
    NodeTypes,
    Question,
    Table,
    TableMetadata,
)


class MetabaseConfig(BaseSettings):
    endpoint: AnyHttpUrl
    username: SecretStr
    password: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, endpoint: str):
        endpoint = endpoint.rstrip("/")
        return parse_obj_as(AnyHttpUrl, endpoint)

    class Config:
        env_prefix = "grai_metabase_"
        env_file = ".env"


class MetabaseAPI:
    """
    Wrapper class for interacting with the Metabase API.

    Args:
        username (str, optional): Metabase username. Defaults to None or returns value from environment variable.
        password (str, optional): Metabase password. Defaults to None or returns value from environment variable.
        endpoint (str, optional): Metabase API endpoint URL. Defaults to None.

    """

    def __init__(
        self,
        username: Optional[str] = None,
        password: Optional[str] = None,
        endpoint: Optional[str] = None,
    ):
        passthrough_kwargs = {
            "username": username,
            "password": password,
            "endpoint": endpoint,
        }

        self.config = MetabaseConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})
        self.api_endpoint = f"{self.config.endpoint}/api"

        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})
        self.session.headers.update(self.authenticate())

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def authenticate(self) -> Dict[str, str]:
        """
        Authenticates the user and sets the session headers.

        Args:
            request (callable): The HTTP request method to use for authentication.
            url (str): The URL for the authentication endpoint.

        Raises:
            ConnectionError: If there is an error connecting to the endpoint.

        """
        try:
            response = requests.post(
                url=f"{self.api_endpoint}/session",
                json={
                    "username": self.config.username.get_secret_value(),
                    "password": self.config.password.get_secret_value(),
                },
            )

            response.raise_for_status()
            return {"X-Metabase-Session": response.json()["id"]}

        except ConnectionError as ce:
            raise ce

    @staticmethod
    def make_request(request: Callable[..., requests.Response], url: str) -> Dict:
        """
        Makes an authenticated API request and returns the JSON response.

        Args:
            request (callable): The HTTP request method to use for the API call.
            url (str): The URL for the API endpoint.

        Returns:
            dict: The JSON response from the API.

        Raises:
            AssertionError: If the response status code is not 200.

        """
        response = request(url=url)
        if response.status_code != 200:
            message = (
                f"While performing a {request.__name__.upper()} operation on `{url}`, "
                f"the Metabase API returned error code `{response.status_code}` with reason `{response.reason}`. "
                f"This does not appear to be an issue with Grai, please check your Metabase instance."
            )
            raise requests.RequestException(message)
        return response.json()

    @staticmethod
    async def async_make_request(request: Callable[..., requests.Response], url: str):
        response = request(url=url)
        if response.status_code != 200:
            message = (
                f"While performing a {request.__name__.upper()} operation on `{url}`, "
                f"the Metabase API returned error code {response.status_code} with `{response.reason}`."
                f"This does not appear to be an issue with Grai, please check your Metabase instance."
            )
            raise requests.RequestException(message)
        return response.json()

    def get_questions(self) -> List[api.Question]:
        """
        Retrieves the list of questions from the Metabase API.

        Returns:

        """
        url = f"{self.api_endpoint}/card"
        return [api.Question(**item) for item in self.make_request(self.session.get, url)]

    def get_tables(self) -> List[api.Table]:
        """
        Retrieves the list of tables from the Metabase API.

        Returns:

        """
        url = f"{self.api_endpoint}/table"
        return [api.Table(**item) for item in self.make_request(self.session.get, url)]

    def get_table_metadata(self, table_id: int) -> api.TableMetadata:
        """A table id to retrieve metadata for from Metabase

        Args:
            table_id: A table id to retrieve metadata for from Metabase.

        Returns:

        """
        url = f"{self.api_endpoint}/table/{table_id}/query_metadata"
        return api.TableMetadata(**self.make_request(self.session.get, url))

    async def get_all_table_metadata(self, table_ids: List[int]) -> List[api.TableMetadata]:
        """

        Args:
            table_ids: A list of table id's to retrieve metadata for from Metabase.

        Returns:

        """
        async with httpx.AsyncClient(headers=self.session.headers) as client:
            urls = [f"{self.api_endpoint}/table/{table_id}/query_metadata" for table_id in table_ids]
            responses = await asyncio.gather(*[client.get(url) for url in urls], return_exceptions=True)

        for i, response in enumerate(responses):
            if not hasattr(response, "status_code") or response.status_code != 200:
                response = self.session.get(url=urls[i])
                assert response.status_code == 200, f"Request error to `{urls[i]}`. Got {response.status_code}"
                responses[i] = response

        return [api.TableMetadata(**response.json()) for response in responses]

    def get_dbs(self) -> List[api.DB]:
        """Retrieves the list of databases from the Metabase API.

        Returns:
            dict: The JSON response containing the list of databases.

        """
        url = f"{self.api_endpoint}/database"
        return [api.DB(**api_resp) for api_resp in self.make_request(self.session.get, url)["data"]]

    def get_collections(self) -> List[api.Collection]:
        """
        Retrieves the list of collections from the Metabase API.

        Returns:
            dict: The JSON response containing the list of collections.

        """

        url = f"{self.api_endpoint}/collection"
        return [api.Collection(**item) for item in self.make_request(self.session.get, url) if item["id"] != "root"]


def build_namespace_map(default_map: Dict[int, str], dbs: Dict[int, api.DB], metabase_namespace: str) -> Dict[int, str]:
    namespace_map = default_map.copy()

    for k, v in dbs.items():
        db_id_ns = f"{metabase_namespace}.{k}.{v.name}"
        namespace_map.setdefault(k, db_id_ns)

    return namespace_map


class NamespaceMapJsonModel(BaseModel):
    json_obj: Json[Dict[int, str]]


class MetabaseConnector(MetabaseAPI):
    """
    Connector class for interacting with Metabase API and building lineage information.

    Args:
        namespaces: A mapping of database IDs to their corresponding namespace names. Defaults to None.
        default_namespace: The default namespace to be used when a table or question does not have a specific namespace. Defaults to None.
        *args: Additional positional arguments to be passed to the base class constructor.
        **kwargs: Additional keyword arguments to be passed to the base class constructor.

    Attributes:
        metabase_namespace (str): The default namespace to be used.
        collections: A list of active collections in Metabase
        questions: A list of non-archived questions returned by Metabase
        tables: The list of tables retrieved from the Metabase API.
        columns: The list of columns referenced by Metabase Questions

        tables_map: A mapping of table IDs to their corresponding table dictionaries.
        dbs_map: A mapping of database IDs to corresponding database responses.
        questions_map: A mapping of question IDs to their corresponding question dictionaries.
        namespace_map: A mapping of database IDs to their corresponding namespace names.
        question_table_map: A mapping of question IDs to their corresponding table IDs.
        table_db_map: A mapping of table IDs to their corresponding database IDs.

    """

    def __init__(
        self,
        metabase_namespace: str,
        namespace_map: Optional[Union[str, Dict[int, str]]] = None,
        *args,
        **kwargs,
    ):
        if namespace_map is None:
            namespace_map = {}
        elif isinstance(namespace_map, str):
            try:
                namespace_map = NamespaceMapJsonModel(json_obj=namespace_map).json_obj
            except Exception as e:
                message = (
                    f"There was an error parsing the value provided in namespace_map. When providing namespace_map "
                    f"it must be either a dictionary whose keys are database id's in metabase and values are namespace "
                    f"strings in Grai for the corresponding database or a JSON string of the same. "
                    f"In this case we received a JSON string but it did not parse to Dict[int, str] as expected."
                )
                raise ValueError(message) from e

        super().__init__(*args, **kwargs)
        self.base_namespace_map = namespace_map
        self.metabase_namespace = metabase_namespace

    @cached_property
    def dbs_map(self) -> Dict[int, api.DB]:
        return {db.id: db for db in self.get_dbs()}

    @cached_property
    def namespace_map(self):
        return build_namespace_map(self.base_namespace_map, self.dbs_map, self.metabase_namespace)

    @cached_property
    def tables(self) -> List[Table]:
        tables = [
            Table(**api_resp.dict(), namespace=self.namespace_map[api_resp.db_id])
            for api_resp in self.get_tables()
            if api_resp.active
        ]
        return tables

    @cached_property
    def tables_map(self) -> Dict[int, Table]:
        return {table.id: table for table in self.tables}

    @cached_property
    def table_metadata_map(self) -> Dict[int, TableMetadata]:
        table_metas = asyncio.run(self.get_all_table_metadata(list(self.tables_map.keys())))
        table_metas = (
            TableMetadata(namespace=table.namespace, **meta.dict())
            for meta, table in zip(table_metas, self.tables_map.values())
        )
        return {meta.id: meta for meta in table_metas}

    @cached_property
    def collections(self) -> List[Collection]:
        collections = [
            Collection.from_orm(api_resp)
            for api_resp in self.get_collections()
            if api_resp.id != "root" and api_resp.archived is False
        ]
        for collection in collections:
            collection.namespace = self.metabase_namespace
        return collections

    @cached_property
    def collections_map(self) -> Dict[int, Collection]:
        return {collection.id: collection for collection in self.collections}

    @cached_property
    def questions(self) -> List[Question]:
        questions = [
            Question(**api_resp.dict(), namespace=self.metabase_namespace)
            for api_resp in self.get_questions()
            if api_resp.archived is False
        ]
        return questions

    @cached_property
    def columns(self):
        seq_of_columns = (
            self.table_metadata_map[question.table_id].get_columns()
            for question in self.questions
            if question.table_id in self.table_metadata_map
        )
        return list(set(chain.from_iterable(seq_of_columns)))

    def get_nodes(self) -> List[NodeTypes]:
        """
        Retrieves the list of nodes representing tables and questions.

        Returns:
            List[NodeTypes]: The list of nodes.

        """

        nodes = chain(self.questions, self.tables, self.collections, self.columns)
        return list(nodes)

    def get_edges(self) -> List[Edge]:
        """
        Retrieves the list of edges representing the relationships between questions and tables.

        Returns:
            List[Edge]: The list of edges.

        """
        question_columns_iter = (
            (question, self.table_metadata_map[question.table_id].get_columns())
            for question in self.questions
            if question.table_id in self.table_metadata_map
        )
        question_column_edge_iter = (
            (Edge(source=column, destination=question, namespace=question.namespace) for column in columns)
            for question, columns in question_columns_iter
        )
        column_to_question_edges = chain.from_iterable(question_column_edge_iter)

        question_to_table_edges = (
            Edge(
                source=question,
                destination=self.tables_map[question.table_id],
                namespace=self.metabase_namespace,
            )
            for question in self.questions
            if question.table_id in self.tables_map
        )

        collection_to_question_edges = (
            Edge(
                source=self.collections_map[question.collection_id],
                destination=question,
                namespace=self.metabase_namespace,
            )
            for question in self.questions
            if question.collection_id in self.collections_map
        )

        edges = list(chain(collection_to_question_edges, question_to_table_edges, column_to_question_edges))

        return edges
