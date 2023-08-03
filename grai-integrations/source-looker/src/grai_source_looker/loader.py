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

from grai_source_looker.models import Dashboard

T = TypeVar("T")
P = ParamSpec("P")


class LookerConfig(BaseSettings):
    """ """

    base_url: str
    client_id: str
    client_secret: SecretStr
    verify_ssl: bool = True

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
    ):
        passthrough_kwargs = {
            "base_url": base_url,
            "client_id": client_id,
            "client_secret": client_secret,
            "verify_ssl": verify_ssl,
        }
        self.config = LookerConfig(**{k: v for k, v in passthrough_kwargs.items() if v is not None})

        settings = LookerSettings(self.config)

        self.sdk = looker_sdk.init40(config_settings=settings)

    def get_dashboards(self):
        result = self.sdk.all_dashboards()

        return [Dashboard(**item) for item in result]

    def get_nodes_and_edges(self):
        nodes = self.get_dashboards()

        return nodes, []
