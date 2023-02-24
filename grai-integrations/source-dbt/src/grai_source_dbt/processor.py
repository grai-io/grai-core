import json
from functools import cached_property
from typing import List, Union

from dbt_artifacts_parser.parser import parse_manifest
from dbt_artifacts_parser.parsers.utils import get_dbt_schema_version
from grai_schemas.v1 import EdgeV1, NodeV1

from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.loaders import MANIFEST_MAP, AllDbtNodeTypes, ManifestTypes
from grai_source_dbt.loaders.base import BaseManifestLoader
from grai_source_dbt.models.grai import Column, Edge


class ManifestProcessor:
    MANIFEST_MAP = MANIFEST_MAP

    def __init__(self, loader: BaseManifestLoader):
        self.loader = loader
        self.namespace = loader.namespace

    @cached_property
    def adapted_nodes(self) -> List[NodeV1]:
        return adapt_to_client(self.loader.nodes, "v1")

    @cached_property
    def adapted_edges(self) -> List[EdgeV1]:
        return adapt_to_client(self.loader.edges, "v1")

    @property
    def nodes(self) -> List[Union[AllDbtNodeTypes, Column]]:
        return self.loader.nodes

    @property
    def edges(self) -> List[Edge]:
        return self.loader.edges

    @property
    def manifest(self) -> ManifestTypes:
        return self.loader.manifest

    @classmethod
    def load(cls, manifest_obj: Union[str, dict], namespace: str) -> "ManifestProcessor":
        if isinstance(manifest_obj, str):
            with open(manifest_obj, "r") as f:
                manifest_dict = json.load(f)
        else:
            manifest_dict = manifest_obj

        version = get_dbt_schema_version(manifest_dict)
        if version not in cls.MANIFEST_MAP:
            message = f"Manifest version {version} not yet supported"
            raise NotImplementedError(message)

        manifest_obj = parse_manifest(manifest_dict)
        manifest = cls.MANIFEST_MAP[version](manifest_obj, namespace)
        return ManifestProcessor(manifest)
