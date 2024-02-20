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


class MeasureSchema(BaseModel):
    name: str
    title: str
    shortTitle: str
    aliasName: str
    type: str
    aggType: str
    drillMembers: list[str]


class DimensionSchema(BaseModel):
    name: str
    title: str
    shortTitle: str
    aliasName: str
    type: str
    suggestFilterValues: bool


class GraiSchema(BaseModel):
    table_name: str
    namespace: str
    column_name: Dict[str, str]


class MetaSchema(BaseModel):
    grai: Optional[GraiSchema]

    class Config(BaseModel.Config):
        extra = "allow"


class CubeSchema(BaseModel):
    name: str
    title: str
    meta: MetaSchema
    measures: List[MeasureSchema]
    dimensions: List[DimensionSchema]
    segments: List
    connectedComponent: int


class MetaResponseSchema(BaseModel):
    cubes: List[CubeSchema]


class CubeAPI:
    """ """

    def __init__(
        self,
        config: Optional[CubeApiConfig] = None,
    ):
        self.config = config if config is not None else CubeApiConfig()
        self.session = requests.Session()
        self.session.auth = TokenAuth(self.config.jwt_token)
        self.session.headers.update({"Accept": "application/json"})

    def call_meta(self) -> MetaResponseSchema:
        """ """
        url = f"{self.config.api_url}/meta"
        response = self.session.get(url)
        response.raise_for_status()
        return MetaResponseSchema.parse_obj(response.json())

    def ready(self) -> requests.Response:
        """ """
        url = f"{self.config.base_url}/readyz"
        response = self.session.get(url)
        return response
