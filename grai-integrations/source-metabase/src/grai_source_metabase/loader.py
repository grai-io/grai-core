import json
from itertools import chain
from typing import Optional, Callable, Dict, List

import requests
from pydantic import BaseSettings, SecretStr, validator
from requests.exceptions import ConnectionError
from retrying import retry

from src.grai_source_metabase.models import Question, Table, NodeTypes, Edge

_endpoint = "https://data.inv.tech/api"


class MetabaseConfig(BaseSettings):
    endpoint: str = _endpoint
    username: SecretStr
    password: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, v):
        return v.rstrip("/")

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

        self.config = MetabaseConfig(
            **{k: v for k, v in passthrough_kwargs.items() if v is not None}
        )

        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

    @retry(stop_max_attempt_number=3, wait_fixed=5000)
    def authenticate(self, request: Callable[..., requests.Response], url: str):
        """
        Authenticates the user and sets the session headers.

        Args:
            request (callable): The HTTP request method to use for authentication.
            url (str): The URL for the authentication endpoint.

        Raises:
            ConnectionError: If there is an error connecting to the endpoint.

        """
        try:
            response = request(
                url=url,
                json={
                    "username": self.config.username.get_secret_value(),
                    "password": self.config.password.get_secret_value(),
                },
            )

            response.raise_for_status()
            self.session.headers.update({"X-Metabase-Session": response.json()["id"]})
        except ConnectionError as ce:
            raise ce

    def make_request(self, request: Callable[..., requests.Response], url: str):
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

        self.authenticate(self.session.post, f"{self.config.endpoint}/session")
        return self.make_request(self.session.get, f"{self.config.endpoint}/card")

    def get_tables(self):
        """
        Retrieves the list of tables from the Metabase API.

        Returns:
            dict: The JSON response containing the list of tables.

        """

        self.authenticate(self.session.post, f"{self.config.endpoint}/session")
        return self.make_request(self.session.get, f"{self.config.endpoint}/table")

    def get_dbs(self):
        """
        Retrieves the list of databases from the Metabase API.

        Returns:
            dict: The JSON response containing the list of databases.

        """

        self.authenticate(self.session.post, f"{self.config.endpoint}/session")
        return self.make_request(self.session.get, f"{self.config.endpoint}/database")

    def get_collections(self):
        """
        Retrieves the list of collections from the Metabase API.

        Returns:
            dict: The JSON response containing the list of collections.

        """

        pass


def build_namespace_map(
    dbs: Dict, namespace_map, default_namespace: Optional[str]
) -> Dict:
    if namespace_map is None and default_namespace is None:
        message = "You must provide either a namespace_map or a default_namespace "

        raise ValueError(message)

    elif isinstance(namespace_map, str):
        namespace_map = json.loads(namespace_map)

    if namespace_map is None:
        namespace_map = {}

    if default_namespace is not None:
        namespace_map = namespace_map.copy()
        for k in dbs.keys():
            namespace_map.setdefault(k, default_namespace)

    return namespace_map


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
        namespaces: Optional[Dict] = None,
        default_namespace: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.default_namespace = default_namespace

        # This line creates a list of tables by modifying each table dictionary obtained from the get_tables() method.
        # It replaces the "schema" key with a new key "schema_name" while preserving the other key-value pairs.
        # this is because the "schema" key is a reserved keyword in the pydantic.
        self.tables = [
            {**table, "schema_name": table.pop("schema")} for table in self.get_tables()
        ]
        self.tables_map = {table["id"]: table for table in self.tables}
        self.dbs_map = {db["id"]: db for db in self.get_dbs()["data"]}
        self.questions_map = {
            question["id"]: question for question in self.get_questions()
        }

        self.namespace_map = build_namespace_map(
            self.dbs_map, namespaces, default_namespace
        )

        self.question_table_map = {}
        self.table_db_map = {}
        self.question_db_map = {}

    def build_lineage(self):
        """
        Builds the lineage information by updating the mappings and maps.

        This method updates the `tables_map`, `dbs_map`, `questions_map`, `question_table_map`, `table_db_map`,
        and `question_db_map` attributes.

        """

        self.question_table_map = {
            question["id"]: question["table_id"]
            for question in self.get_questions()
            if question["table_id"] and question["archived"] is False
        }

        self.table_db_map = {table["id"]: table["db_id"] for table in self.tables}

        for question, table in self.question_table_map.items():
            self.question_db_map[question] = self.table_db_map[table]

    def get_nodes(self) -> List[NodeTypes]:
        """
        Retrieves the list of nodes representing tables and questions.

        Returns:
            List[NodeTypes]: The list of nodes.

        """

        for question in self.questions_map.values():
            question["namespace"] = self.namespace_map[
                self.question_db_map[question["id"]]
            ]

        for table in self.tables_map.values():
            table["namespace"] = self.namespace_map[self.table_db_map[table["id"]]]

        nodes = chain(
            chain.from_iterable(Table(**table) for table in self.tables_map.values()),
            chain.from_iterable(
                Question(**question) for question in self.questions_map.values()
            ),
        )

        return list(nodes)

    def get_edges(self) -> List[Edge]:
        """
        Retrieves the list of edges representing the relationships between questions and tables.

        Returns:
            List[Edge]: The list of edges.

        """

        edges = []
        for question, table in self.question_table_map.items():
            edges.append(
                Edge(
                    source=Question(**self.questions_map[question]),
                    target=Table(**self.tables_map[table]),
                    label="question_table",
                    namespace=self.namespace_map[self.question_db_map[question]],
                )
            )

        return edges
