from functools import cached_property
from itertools import chain
from typing import Callable, Dict, List, Optional, TypedDict, Union

import requests
from pydantic import (
    BaseModel,
    BaseSettings,
    HttpUrl,
    Json,
    SecretStr,
    parse_obj_as,
    validator,
)
from requests.exceptions import ConnectionError
from retrying import retry

from grai_source_metabase.models import Edge, NodeTypes, Question, Table


class MetabaseConfig(BaseSettings):
    endpoint: HttpUrl
    username: SecretStr
    password: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, endpoint: str):
        endpoint = endpoint.rstrip("/")
        return parse_obj_as(HttpUrl, endpoint)

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
    def make_request(request: Callable[..., requests.Response], url: str):
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
        assert response.status_code == 200
        return response.json()

    def get_questions(self):
        """
        Retrieves the list of questions from the Metabase API.

        Returns:
            dict: The JSON response containing the list of questions.

        """
        url = f"{self.api_endpoint}/card"
        return self.make_request(self.session.get, url)

    def get_tables(self):
        """
        Retrieves the list of tables from the Metabase API.

        Returns:
            dict: The JSON response containing the list of tables.

        """
        url = f"{self.api_endpoint}/table"
        return self.make_request(self.session.get, url)

    def get_dbs(self):
        """
        Retrieves the list of databases from the Metabase API.

        Returns:
            dict: The JSON response containing the list of databases.

        """
        url = f"{self.api_endpoint}/database"
        return self.make_request(self.session.get, url)

    def get_collections(self):
        """
        Retrieves the list of collections from the Metabase API.

        Returns:
            dict: The JSON response containing the list of collections.

        """

        pass


def build_namespace_map(default_map: Dict[int, str], dbs: Dict, metabase_namespace: str) -> Dict[int, str]:
    namespace_map = default_map.copy()

    for k, v in dbs.items():
        db_id_ns = f"{metabase_namespace}.{k}.{v['name']}"
        namespace_map.setdefault(k, db_id_ns)

    return namespace_map


class NamespaceMapJsonModel(BaseModel):
    json_obj: Json[Dict[int, str]]


class MetabaseConnector(MetabaseAPI):
    """
    Connector class for interacting with Metabase API and building lineage information.

    Args:
        namespaces (Dict, optional): A mapping of database IDs to their corresponding namespace names. Defaults to None.
        default_namespace (str, optional): The default namespace to be used when a table or question does not have a specific namespace. Defaults to None.
        *args: Additional positional arguments to be passed to the base class constructor.
        **kwargs: Additional keyword arguments to be passed to the base class constructor.

    Attributes:
        default_namespace (str): The default namespace to be used.
        tables (List[Dict]): The list of tables retrieved from the Metabase API.
        tables_map (Dict[int, Dict]): A mapping of table IDs to their corresponding table dictionaries.
        dbs_map (Dict[int, Dict]): A mapping of database IDs to their corresponding database dictionaries.
        questions_map (Dict[int, Dict]): A mapping of question IDs to their corresponding question dictionaries.
        namespace_map (Dict[int, str]): A mapping of database IDs to their corresponding namespace names.
        question_table_map (Dict[int, int]): A mapping of question IDs to their corresponding table IDs.
        table_db_map (Dict[int, int]): A mapping of table IDs to their corresponding database IDs.
        question_db_map (Dict[int, int]): A mapping of question IDs to their corresponding database IDs.

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
    def namespace_map(self):
        return build_namespace_map(self.base_namespace_map, self.dbs_map, self.metabase_namespace)

    @cached_property
    def tables(self) -> List[Dict]:
        # This line creates a list of tables by modifying each table dictionary obtained from the get_tables() method.
        # It replaces the "schema" key with a new key "schema_name" while preserving the other key-value pairs.
        # this is because the "schema" key is a reserved keyword in the pydantic.
        return [{**table, "schema_name": table.pop("schema")} for table in self.get_tables()]

    @cached_property
    def tables_map(self) -> Dict:
        return {table["id"]: table for table in self.tables if table["active"]}

    @cached_property
    def dbs_map(self) -> Dict:
        return {db["id"]: db for db in self.get_dbs()["data"]}

    @cached_property
    def questions_map(self) -> Dict:
        return {question["id"]: question for question in self.get_questions() if question["archived"] is False}

    @cached_property
    def question_table_map(self) -> Dict:
        return {
            question["id"]: question["table_id"]
            for question in self.questions_map.values()
            if question["table_id"] and self.tables_map.get(question["table_id"]) is not None
        }

    @cached_property
    def table_db_map(self) -> Dict:
        return {
            table["id"]: table["db_id"]
            for table in self.tables
            if table["id"] is not None and table["db_id"] is not None
        }

    def get_nodes(self) -> List[NodeTypes]:
        """
        Retrieves the list of nodes representing tables and questions.

        Returns:
            List[NodeTypes]: The list of nodes.

        """

        for question in self.questions_map.values():
            question["namespace"] = self.metabase_namespace

        for table in self.tables_map.values():
            table["namespace"] = self.namespace_map[self.table_db_map[table["id"]]]

        verified_questions = [Question(**question) for question in self.questions_map.values()]
        verified_tables = [Table(**table) for table in self.tables_map.values()]
        nodes = chain(verified_questions, verified_tables)

        return list(nodes)

    def get_edges(self) -> List[Edge]:
        """
        Retrieves the list of edges representing the relationships between questions and tables.

        Returns:
            List[Edge]: The list of edges.

        """
        edges = (
            Edge(
                source=Question(**self.questions_map[question]),
                destination=Table(**self.tables_map[table]),
                namespace=self.questions_map[question]["namespace"],
            )
            for question, table in self.question_table_map.items()
        )
        return list(edges)
