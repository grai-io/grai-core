import datetime
import random
from typing import Optional

import jwt
import requests
from grai_schemas.v1.mock import MockSource
from grai_source_cube.api import BaseCubeAPI, CubeSchema, GraiSchema, MetaResponseSchema
from grai_source_cube.base import CubeIntegration
from grai_source_cube.connector import CubeConnector, NamespaceMap
from grai_source_cube.settings import CubeApiConfig
from grai_source_cube.types import (
    CubeEdgeColumnToColumn,
    CubeEdgeTableToColumn,
    CubeEdgeTableToTable,
    CubeNode,
    DimensionNode,
    GraiID,
    MeasureNode,
    SourceColumnNode,
    SourceNode,
    SourceTableNode,
)
from polyfactory.decorators import post_generated
from polyfactory.factories.pydantic_factory import ModelFactory
from pydantic import SecretStr


class SourceNodeFactory(ModelFactory[SourceNode]):
    pass


class SourceTableNodeFactory(ModelFactory[SourceTableNode]):
    pass


class GraiIDFactory(ModelFactory[GraiID]):
    pass


class SourceColumnNodeFactory(ModelFactory[SourceColumnNode]):
    pass


class CubeNodeFactory(ModelFactory[CubeNode]):
    pass


class DimensionNodeFactory(ModelFactory[DimensionNode]):
    pass


class MeasureNodeFactory(ModelFactory[MeasureNode]):
    pass


class CubeEdgeTableToColumnFactory(ModelFactory[CubeEdgeTableToColumn]):
    pass


class CubeEdgeTableToTableFactory(ModelFactory[CubeEdgeTableToTable]):
    pass


class CubeEdgeColumnToColumnFactory(ModelFactory[CubeEdgeColumnToColumn]):
    pass


class NamespaceMapFactory(ModelFactory[NamespaceMap]):
    __set_as_default_factory_for_type__ = True


class CubeApiConfigFactory(ModelFactory[CubeApiConfig]):
    __set_as_default_factory_for_type__ = True
    api_url: str = "http://localhost:8080/v1"

    @post_generated
    @classmethod
    def api_token(cls, api_secret: Optional[SecretStr]) -> Optional[SecretStr]:
        """ """
        if api_secret is None:
            payload = {"exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)}
            encoded_jwt = jwt.encode(payload, "mock_secret", algorithm="HS256")
            response = SecretStr(encoded_jwt)
        elif random.Random().choice([True, False]):
            response = None
        else:
            payload = {"exp": datetime.datetime.now(datetime.UTC) + datetime.timedelta(days=1)}
            encoded_jwt = jwt.encode(payload, api_secret, algorithm="HS256")
            response = SecretStr(encoded_jwt)

        return response


class GraiSchemaFactory(ModelFactory[GraiSchema]):
    __set_as_default_factory_for_type__ = True


class CubeSchemaFactory(ModelFactory[CubeSchema]):
    __set_as_default_factory_for_type__ = True
    grai_meta: GraiSchema = GraiSchemaFactory


class MetaResponseSchemaFactory(ModelFactory[MetaResponseSchema]):
    __set_as_default_factory_for_type__ = True


class MockCubeAPI(BaseCubeAPI):
    def meta(self) -> MetaResponseSchema:
        return MetaResponseSchemaFactory.build()

    def ready(self) -> requests.Response:
        response = requests.Response()
        response.status_code = 200
        response._content = b"Success"
        return response


class MockConnector(CubeConnector):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("config", CubeApiConfigFactory.build())
        kwargs.setdefault("namespace", "mock_namespace")
        super().__init__(*args, **kwargs)

        self.mocked_api = MockCubeAPI()

        for attr_name in dir(BaseCubeAPI):
            if attr_name.startswith("_"):
                continue

            attr = getattr(self.mocked_api, attr_name)
            if callable(attr):
                setattr(self, attr_name, attr)


class MockCubeIntegration(CubeIntegration):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("config", CubeApiConfigFactory.build())
        kwargs.setdefault("source", MockSource().source())
        kwargs.setdefault("namespace", "mock_namespace")
        super().__init__(*args, **kwargs)

        self.connector = MockConnector(namespace=kwargs["namespace"], config=kwargs["config"])
