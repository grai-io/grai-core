import json
from itertools import chain
from typing import Callable, Dict, List, Optional, Union

import requests
from pydantic import BaseSettings, SecretStr, validator
from requests.exceptions import ConnectionError
from retrying import retry

from grai_source_metabase.models import Edge, NodeTypes, Question, Table


class MetabaseConfig(BaseSettings):
    endpoint: str
    username: SecretStr
    password: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, endpoint: str):
        endpoint = endpoint.rstrip("/")
        return endpoint

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


def build_namespace_map(dbs: Dict, namespace_map: Union[str, Dict, None], metabase_namespace: str) -> Dict:
    if isinstance(namespace_map, str):
        namespace_map = json.loads(namespace_map)
    elif namespace_map is None:
        namespace_map = {}

    for k, v in dbs.items():
        db_id_ns = f"{metabase_namespace}.{k}.{v['name']}"
        namespace_map.setdefault(k, db_id_ns)

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
        metabase_namespace: str,
        namespaces: Optional[Dict] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)
        self._lineage_ready = False
        self.metabase_namespace = metabase_namespace

        # This line creates a list of tables by modifying each table dictionary obtained from the get_tables() method.
        # It replaces the "schema" key with a new key "schema_name" while preserving the other key-value pairs.
        # this is because the "schema" key is a reserved keyword in the pydantic.
        self.tables = [{**table, "schema_name": table.pop("schema")} for table in self.get_tables()]
        self.tables_map = {table["id"]: table for table in self.tables if table["active"]}
        self.dbs_map = {db["id"]: db for db in self.get_dbs()["data"]}

        self.questions_map = {
            question["id"]: question for question in self.get_questions() if question["archived"] is False
        }
        self.namespace_map = build_namespace_map(self.dbs_map, namespaces, self.metabase_namespace)

        self.question_table_map = {}
        self.table_db_map = {}
        # self.question_db_map = {}

    def build_lineage(self):
        """
        Builds the lineage information by updating the mappings and maps.

        This method updates the `tables_map`, `dbs_map`, `questions_map`, `question_table_map`, `table_db_map`,
        and `question_db_map` attributes.

        """

        self.question_table_map = {
            question["id"]: question["table_id"]
            for question in self.questions_map.values()
            if question["table_id"] and self.tables_map.get(question["table_id"]) is not None
        }

        self.table_db_map = {
            table["id"]: table["db_id"]
            for table in self.tables
            if table["id"] is not None and table["db_id"] is not None
        }

        # for question, table in self.question_table_map.items():
        #     self.question_db_map[question] = self.table_db_map[table]

        self._lineage_ready = True

    def get_nodes(self) -> List[NodeTypes]:
        """
        Retrieves the list of nodes representing tables and questions.

        Returns:
            List[NodeTypes]: The list of nodes.

        """

        if not self._lineage_ready:
            self.build_lineage()

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

        if not self._lineage_ready:
            self.build_lineage()

        edges = (
            Edge(
                source=Question(**self.questions_map[question]),
                destination=Table(**self.tables_map[table]),
                namespace=self.questions_map[question]["namespace"],
            )
            for question, table in self.question_table_map.items()
        )
        return list(edges)
