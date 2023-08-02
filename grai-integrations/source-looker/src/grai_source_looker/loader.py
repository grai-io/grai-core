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


class Loader(api_settings.ApiSettings):
    pass
