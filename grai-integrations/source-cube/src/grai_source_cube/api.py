from abc import ABC, abstractmethod
from typing import List, Optional

import requests
from grai_source_cube.settings import CubeApiConfig
from pydantic import BaseModel
from requests.auth import AuthBase


class TokenAuth(AuthBase):
    """Implements a custom authentication scheme."""

    def __init__(self, token):
        self.token = token

    def __call__(self, r):
        # Add an Authorization header with the token
        r.headers["Authorization"] = f"Bearer {self.token}"
        return r


class DrillMembersGroupedSchema(BaseModel):
    measures: List
    dimensions: List


class MeasureSchema(BaseModel):
    name: str
    title: str
    shortTitle: str
    cumulative: bool
    cumulativeTotal: bool
    type: str
    aggType: str
    drillMembers: list[str]
    drillMembersGrouped: DrillMembersGroupedSchema
    isVisible: bool
    public: bool


class DimensionSchema(BaseModel):
    name: str
    title: str
    type: str
    shortTitle: str
    type: str
    suggestFilterValues: bool
    isVisible: bool
    public: bool
    primaryKey: bool


class JoinSchema(BaseModel):
    relationship: str
    sql: str
    name: str


class GraiSchema(BaseModel):
    source_namespace: str
    table_name: Optional[str]

    # column_name: Dict[str, str] = {}

    class Config:
        extra = "allow"


class CubeMeta(BaseModel):
    grai: Optional[GraiSchema]

    class Config:
        extra = "allow"


class CubeSchema(BaseModel):
    name: str
    type: str
    title: str
    isVisible: bool
    public: bool
    measures: List[MeasureSchema]
    dimensions: List[DimensionSchema]
    segments: List
    connectedComponent: Optional[int]
    sql: Optional[str]
    meta: CubeMeta = CubeMeta()
    fileName: Optional[str]
    preAggregations: List
    joins: List[JoinSchema]

    class Config:
        extra = "allow"


class MetaResponseSchema(BaseModel):
    cubes: List[CubeSchema]


class BaseCubeAPI(ABC):
    """ """

    @abstractmethod
    def meta(self) -> MetaResponseSchema:
        """ """
        pass

    @abstractmethod
    def ready(self) -> requests.Response:
        """ """
        pass


class CubeAPI(BaseCubeAPI):
    """ """

    def __init__(
        self,
        config: Optional[CubeApiConfig] = None,
    ):
        if config is None:
            try:
                config = CubeApiConfig()
            except Exception as e:
                message = (
                    "Could not instantiate a default connection configuration from available environment variables."
                    "Please provide a valid `config` argument or set the required environment variables."
                )
                raise ValueError(message) from e
        self.config = config if config is not None else CubeApiConfig()
        self.session = requests.Session()
        self.session.auth = TokenAuth(self.config.jwt_token)
        self.session.headers.update({"Accept": "application/json"})

    def meta(self) -> MetaResponseSchema:
        """ """
        url = f"{self.config.api_url}/meta?extended"
        response = self.session.get(url)
        response.raise_for_status()
        return MetaResponseSchema(**response.json())

    def ready(self) -> requests.Response:
        """ """
        url = f"{self.config.base_url}/readyz"
        response = self.session.get(url)
        return response
