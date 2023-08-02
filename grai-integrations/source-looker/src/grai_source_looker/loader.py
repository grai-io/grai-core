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
from grai_source_fivetran.models import (
    Column,
    Edge,
    NamespaceIdentifier,
    NodeTypes,
    Table,
)
from looker_sdk import api_settings
from pydantic import BaseModel, BaseSettings, Json, SecretStr, validator

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

        self.session = requests.Session()
        self.session.auth = (
            self.config.api_key.get_secret_value(),
            self.config.api_secret.get_secret_value(),
        )
        self.session.headers.update({"Accept": "application/json"})
        self.session.params.update({"limit": 10000 if limit is None else limit})
