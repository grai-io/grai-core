import json
from itertools import chain
from typing import Optional, Callable, Dict, List

import requests
from pydantic import BaseSettings, SecretStr, validator
from requests.exceptions import ConnectionError
from retrying import retry

from models import Question, Table, NodeTypes


class MetabaseConfig(BaseSettings):
    endpoint: str = "https://data.inv.tech/api"
    username: SecretStr
    password: SecretStr

    @validator("endpoint")
    def validate_endpoint(cls, v):
        return v.rstrip("/")

    class Config:
        env_prefix = "metabase_"
        env_file = ".env"


class MetabaseAPI:
    """ """

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
        response = request(url=url)
        assert response.status_code == 200
        return response.json()

    def get_questions(self):
        self.authenticate(self.session.post, f"{self.config.endpoint}/session")
        return self.make_request(self.session.get, f"{self.config.endpoint}/card")

    def get_tables(self):
        self.authenticate(self.session.post, f"{self.config.endpoint}/session")
        return self.make_request(self.session.get, f"{self.config.endpoint}/table")

    def get_dbs(self):
        self.authenticate(self.session.post, f"{self.config.endpoint}/session")
        return self.make_request(self.session.get, f"{self.config.endpoint}/database")

    # def get_collections(self):
    #     pass


def build_namespace_map_metabase(
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
    def __init__(
        self,
        namespaces: Optional[Dict] = None,
        default_namespace: Optional[str] = None,
        *args,
        **kwargs,
    ):
        super().__init__(*args, **kwargs)

        self.default_namespace = default_namespace

        self.tables_map = {table["id"]: table for table in self.get_tables()}
        self.dbs_map = {db["id"]: db for db in self.get_dbs()["data"]}
        self.questions_map = {
            question["id"]: question for question in self.get_questions()
        }

        self.namespace_map = build_namespace_map_metabase(
            self.dbs_map, namespaces, default_namespace
        )

        self.question_table_map = {}
        self.table_db_map = {}
        self.question_db_map = {}

    def build_lineage(self):
        self.tables_map.update({table["id"]: table for table in self.get_tables()})
        self.dbs_map.update({db["id"]: db for db in self.get_dbs()["data"]})
        self.questions_map.update(
            {question["id"]: question for question in self.get_questions()}
        )

        self.question_table_map = {
            question["id"]: question["table_id"]
            for question in self.get_questions()
            if question["table_id"] and question["archived"] is False
        }

        self.table_db_map = {table["id"]: table["db_id"] for table in self.get_tables()}

        for question, table in self.question_table_map.items():
            self.question_db_map[question] = self.table_db_map[table]

    def get_nodes(self) -> List[NodeTypes]:
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


# if __name__ == "__main__":
#     mb = MetabaseConnector()
#     mb.build_lineage()
#     print(mb.questions_map)
# print(mb.question_table_map)
# print(mb.table_db_map)
# print(mb.question_db_map)
#     mb = MetabaseAPI()
#     print(mb.get_dbs())
