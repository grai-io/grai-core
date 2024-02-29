from abc import ABC, abstractmethod
from typing import Dict, List, Optional

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


class GraiSchema(BaseModel):
    table_name: str
    namespace: str
    column_name: Dict[str, str]


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

    # grai components
    grai_meta: Optional[GraiSchema]


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
