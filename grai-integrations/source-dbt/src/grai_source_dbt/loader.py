import json

from dbt_artifacts_parser.parser import parse_manifest
from dbt_artifacts_parser.parsers.utils import get_dbt_schema_version
from dbt_artifacts_parser.parsers.version_map import ArtifactTypes

from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.versions.base import BaseManifestLoader
from grai_source_dbt.versions.v5 import ManifestLoaderV5


class ManifestProcessor:
    def __init__(self, loader: BaseManifestLoader):
        self.loader = loader

    @property
    def adapted_nodes(self):
        return adapt_to_client(self.loader.nodes, "v1")

    @property
    def adapted_edges(self):
        return adapt_to_client(self.loader.edges, "v1")

    @property
    def nodes(self):
        return self.loader.nodes

    @property
    def edges(self):
        return self.loader.edges

    @property
    def manifest(self):
        return self.loader.manifest


class Manifest:
    manifest_map = {ArtifactTypes.MANIFEST_V5.value.dbt_schema_version: ManifestLoaderV5}

    @classmethod
    def load(cls, file: str, namespace: str) -> ManifestProcessor:
        with open(file, "r") as f:
            manifest_dict = json.load(f)

        version = get_dbt_schema_version(manifest_dict)
        if version not in cls.manifest_map:
            message = f"Manifest version {version} not yet supported"
            raise NotImplementedError(message)

        manifest_obj = parse_manifest(manifest_dict)
        manifest = cls.manifest_map[version](manifest_obj, namespace)
        return ManifestProcessor(manifest)
