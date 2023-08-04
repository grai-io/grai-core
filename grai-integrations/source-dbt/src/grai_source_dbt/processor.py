import json
import warnings
from functools import cached_property
from typing import List, Union

from dbt_artifacts_parser.parser import parse_manifest
from dbt_artifacts_parser.parsers.utils import get_dbt_schema_version
from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.source import SourceSpec

from grai_source_dbt.adapters import adapt_to_client
from grai_source_dbt.loaders import MANIFEST_MAP, AllDbtNodeTypes, ManifestTypes
from grai_source_dbt.loaders.base import BaseManifestLoader
from grai_source_dbt.models.grai import Column, Edge


class ManifestProcessor:
    """ """

    MANIFEST_MAP = MANIFEST_MAP

    source: SourceSpec

    def __init__(self, loader: BaseManifestLoader, source: SourceSpec, strict_mode: bool = False):
        self.loader = loader
        self.namespace = loader.namespace
        self.source = source
        self.strict_mode = strict_mode

    @cached_property
    def adapted_nodes(self) -> List[SourcedNodeV1]:
        """

        Args:

        Returns:

        Raises:

        """
        return adapt_to_client(self.loader.nodes, self.source, "v1")

    @cached_property
    def adapted_edges(self) -> List[SourcedEdgeV1]:
        """

        Args:

        Returns:

        Raises:

        """
        return adapt_to_client(self.loader.edges, self.source, "v1")

    @property
    def nodes(self) -> List[Union[AllDbtNodeTypes, Column]]:
        """

        Args:

        Returns:

        Raises:

        """
        return self.loader.nodes

    @property
    def edges(self) -> List[Edge]:
        """

        Args:

        Returns:

        Raises:

        """
        return self.loader.edges

    @property
    def manifest(self) -> ManifestTypes:
        """

        Args:

        Returns:

        Raises:

        """
        return self.loader.manifest

    @classmethod
    def load(
        cls, manifest_obj: Union[str, dict], namespace: str, source: SourceSpec, strict_mode: bool = False
    ) -> "ManifestProcessor":
        """

        Args:
            manifest_obj:
            namespace:
            source:
            strict_mode:

        Returns:

        Raises:

        """
        if isinstance(manifest_obj, str):
            with open(manifest_obj, "r") as f:
                manifest_dict = json.load(f)
        else:
            manifest_dict = manifest_obj

        version = get_dbt_schema_version(manifest_dict)

        if version not in cls.MANIFEST_MAP and not strict_mode:
            latest_supported_version = list(cls.MANIFEST_MAP.keys())[-1]
            version_label = latest_supported_version.split("/")[-1].split(".")[0]
            warnings.warn(
                f"dbt manifest version {version} is not yet supported. We will attempt to parse the manifest as"
                f"version {version_label} as a fallback. If you see this message please open an issue at"
                f"www.github.com/grai-io/grai-core/issues/new"
            )
            version = latest_supported_version

        manifest_obj = parse_manifest(manifest_dict)
        manifest = cls.MANIFEST_MAP[version](manifest_obj, namespace)

        return ManifestProcessor(manifest, source)
