import asyncio
import json
from itertools import chain
from typing import (
    Any,
    Callable,
    Dict,
    Iterable,
    List,
    Optional,
    ParamSpec,
    Sequence,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
)

import looker_sdk
import requests
from looker_sdk import api_settings
from pydantic import BaseModel, BaseSettings, Json, SecretStr, validator

from grai_source_looker.models import (
    Constraint,
    Dashboard,
    Edge,
    Explore,
    FieldID,
    TableID,
)

T = TypeVar("T")
P = ParamSpec("P")


class LookerConfig(BaseSettings):
    """ """

    base_url: str
    client_id: str
    client_secret: SecretStr
    verify_ssl: bool = True
    namespace: str = "default"

    @validator("base_url")
    def validate_endpoint(cls, value):
        """

        Args:
            value:

        Returns:

        Raises:

        """
        if (trailing_loc := value.find("/api")) > 0:
            value = value[0:trailing_loc]
        return value.rstrip("/")

    class Config:
        """ """

        env_prefix = "grai_looker_"
        env_file = ".env"


class LookerSettings(api_settings.ApiSettings):
    def __init__(self, config: LookerConfig, *args, **kw_args):
        self.config = config

        super().__init__(*args, **kw_args)

    def read_config(self) -> api_settings.SettingsConfig:
        config = super().read_config()

        config["base_url"] = self.config.base_url
        config["client_id"] = self.config.client_id
        config["client_secret"] = self.config.client_secret.get_secret_value()
        config["verify_ssl"] = "true" if self.config.verify_ssl else "false"

        return config


# API authentication docs: https://cloud.google.com/looker/docs/api-auth
# other docs https://cloud.google.com/looker/docs/reference/looker-api/latest/methods/Board/all_boards
# sdk: https://github.com/looker-open-source/sdk-codegen/tree/main/python
class LookerAPI:
    """ """

    def __init__(
        self,
        base_url: Optional[str] = None,
        client_id: Optional[str] = None,
        client_secret: Optional[str] = None,
        verify_ssl: Optional[bool] = None,
        namespace: Optional[str] = None,
    ):
        passthrough_kwargs = {
            "base_url": base_url,
            "client_id": client_id,
            "client_secret": client_secret,
            "verify_ssl": verify_ssl,
            "namespace": namespace,
        }
        self.config = LookerConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})

        settings = LookerSettings(self.config)

        self.sdk = looker_sdk.init40(config_settings=settings)

    def get_dashboards(self):
        result = self.sdk.all_dashboards()

        return [
            Dashboard(namespace=self.config.namespace, **self.sdk.dashboard(item.id))
            for item in result
            if item.id in ["4"]
        ]

    def get_model_explore(self, lookml_model_name: str, explore_name: str):
        return Explore(
            namespace=self.config.namespace,
            **self.sdk.lookml_model_explore(lookml_model_name, explore_name),
        )

    def get_user(self):
        return self.sdk.me()

    def get_nodes_and_edges(self):
        dashboards = self.get_dashboards()

        queries = []
        edges = []

        for dashboard in dashboards:
            q = dashboard.get_queries()
            queries.extend(q)
            edges.extend(dashboard.get_query_edges())

            for query in q:
                explore = self.get_model_explore(query.model, query.view)

                if not explore:
                    print("Explore not found")
                    continue

                queries.append(explore)

                for field in query.fields:
                    dynamic_field = query.dynamic_fields_map.get(field, None)

                    if dynamic_field:
                        field = dynamic_field

                    dimension = next(
                        (dimension for dimension in explore.fields.dimensions if dimension.name == field),
                        None,
                    )

                    if not dimension:
                        print(f"Dimension not found {field}")
                        continue

                    dimension.namespace = self.config.namespace
                    dimension.table_name = explore.table_name

                    queries.append(dimension)

                    edge = Edge(
                        constraint_type=Constraint("bt"),
                        source=TableID(
                            name=explore.table_name,
                            namespace=self.config.namespace,
                        ),
                        destination=FieldID(
                            table_name=explore.table_name,
                            name=dimension.column_name,
                            namespace=self.config.namespace,
                        ),
                    )

                    edges.append(edge)

                    edge = Edge(
                        constraint_type=Constraint("f"),
                        source=FieldID(
                            table_name=explore.table_name,
                            name=dimension.column_name,
                            namespace=self.config.namespace,
                        ),
                        destination=FieldID(
                            table_name=dashboard.name,
                            name=query.title if query.title else query.id,
                            namespace=self.config.namespace,
                        ),
                    )

                    edges.append(edge)

        dashboards.extend(queries)

        return dashboards, edges
