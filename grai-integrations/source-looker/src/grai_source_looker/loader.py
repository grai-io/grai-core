from functools import cached_property
from itertools import chain
from typing import Dict, List, Optional

import looker_sdk
from looker_sdk import api_settings
from pydantic import BaseSettings, SecretStr, validator

from grai_source_looker.models import (
    Constraint,
    Dashboard,
    Edge,
    Explore,
    FieldID,
    TableID,
)


class LookerConfig(BaseSettings):
    """ """

    base_url: str
    client_id: str
    client_secret: SecretStr
    verify_ssl: bool = True
    namespace: str = None
    namespaces: Dict[str, str] = {}

    @validator("base_url")
    def validate_base_url(cls, value):
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
        namespaces: Optional[Dict[str, str]] = None,
    ):
        passthrough_kwargs = {
            "base_url": base_url,
            "client_id": client_id,
            "client_secret": client_secret,
            "verify_ssl": verify_ssl,
            "namespace": namespace,
            "namespaces": namespaces,
        }
        self.config = LookerConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})

        settings = LookerSettings(self.config)

        self.sdk = looker_sdk.init40(config_settings=settings)

    def get_model_explore(self, lookml_model_name: str, explore_name: str, namespace: str) -> Explore:
        return Explore(
            namespace=namespace,
            **self.sdk.lookml_model_explore(lookml_model_name, explore_name),
        )

    @cached_property
    def dashboards(self) -> List[Dashboard]:
        result = self.sdk.all_dashboards()
        return [Dashboard(namespace=self.config.namespace, **self.sdk.dashboard(item.id)) for item in result]

    @cached_property
    def queries(self) -> List:
        query_items = (dashboard.get_queries() for dashboard in self.dashboards)
        return list(chain(*query_items))

    @cached_property
    def explores(self) -> List:
        explores = (self.get_model_explore(query.model, query.view, self.config.namespace) for query in self.queries)
        return [explore for explore in explores if explore]

    def get_user(self):
        return self.sdk.me()

    def get_nodes_and_edges(self):
        nodes = [*self.dashboards, *self.queries]
        edges = list(chain.from_iterable(dashboard.get_query_edges() for dashboard in self.dashboards))

        for query in self.queries:
            # Fetch custom explore namespace or use default
            explore_namespace = self.config.namespaces.get(query.model, self.config.namespace)

            explore = self.get_model_explore(query.model, query.view, explore_namespace)
            # TODO: Typing doesn't make sense here. How can `get_model_explore` return false-y without erroring?
            if not explore:
                print("Explore not found")
                continue

            nodes.append(explore)

            for field in query.fields:
                dynamic_field = query.dynamic_fields_map.get(field, None)

                if dynamic_field:
                    field = dynamic_field

                field_dimension = (dimension for dimension in explore.fields.dimensions if dimension.name == field)

                if not (dimension := next(field_dimension, False)):
                    print(f"Dimension not found {field}")
                    print(query.dynamic_fields)
                    continue

                dimension.namespace = explore_namespace
                dimension.table_name = explore.table_name

                nodes.append(dimension)

                # TODO: Do these reference tables in their storage database or Looker specific constructs?
                # We may not need to generate these edges if they correspond to the storage media but in that case
                # we would need to provide a different namespace from the namespace_map
                edge = Edge(
                    constraint_type=Constraint("bt"),
                    source=TableID(
                        name=explore.table_name,
                        namespace=explore_namespace,
                    ),
                    destination=FieldID(
                        table_name=explore.table_name,
                        name=dimension.column_name,
                        namespace=explore_namespace,
                    ),
                )

                edges.append(edge)

                edge = Edge(
                    constraint_type=Constraint("f"),
                    source=FieldID(
                        table_name=explore.table_name,
                        name=dimension.column_name,
                        namespace=explore_namespace,
                    ),
                    destination=FieldID(
                        table_name=query.dashboard_name,
                        name=query.title if query.title else query.id,
                        namespace=self.config.namespace,
                    ),
                )

                edges.append(edge)

        return nodes, edges
