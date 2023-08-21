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

from grai_source_cube.models import Edge


class CubeConfig(BaseSettings):
    # A config object containing authentication credentials for the cube.js API
    # This will facilitate the creation of a cube.js client object particularly when used in conjunction with
    # environment variables or .env files

    class Config:
        env_prefix = "grai_cube_"
        env_file = ".env"


class CubeAPI:
    """
    Base class for interacting with the cube.js API.
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

        self.config = CubeConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})

        self.session = requests.Session()
        self.session.headers.update({"Content-Type": "application/json"})

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
        assert response.status_code == 200
        return response.json()

    # Additional methods as needed for querying from the API


def build_namespace_map(default_map: Dict[int, str], dbs: Dict[int, api.DB], cube_namespace: str) -> Dict[int, str]:
    """
    Cube potentially knows about data in multiple different databases. Each of those databases could have been added to
    Grai already. We want to make sure those references are assigned to the correct Grai namespace.
    To that end, we create a user defined map between the id used in Cube and the Namespace in Grai.
    This function populates default namespace values for any databases not provided by the user.
    """
    namespace_map = default_map.copy()

    for k, v in dbs.items():
        db_id_ns = f"{cube_namespace}.{k}.{v.name}"
        namespace_map.setdefault(k, db_id_ns)

    return namespace_map


class NamespaceMapJsonModel(BaseModel):
    json_obj: Json[Dict[int, str]]


class CubeConnector(CubeAPI):
    """
    This is an instance of the CubeAPI which knows how to speak "Grai." It is responsible for using
    the cube.js API to retrieve nodes and edges for the graph.
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

    def get_nodes(self) -> List[NodeTypes]:
        """
        Retrieves the list of nodes representing tables and questions.

        Returns:
            List[NodeTypes]: The list of nodes.

        """

        # this is just an example, you can create this however is sensible for Cube
        nodes = chain(self.questions, self.tables, self.collections, self.columns)
        return list(nodes)

    def get_edges(self) -> List[Edge]:
        """
        Retrieves the list of edges representing the relationships between questions and tables.

        Returns:
            List[Edge]: The list of edges.

        """

        # this is just an example, you can create this however is sensible for Cube
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
