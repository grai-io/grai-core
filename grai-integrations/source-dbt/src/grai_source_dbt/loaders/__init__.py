from typing import Type, Union, get_args

from dbt_artifacts_parser.parsers.version_map import ArtifactTypes

from grai_source_dbt.loaders import (
    base,
    utils,
    v1,
    v2,
    v3,
    v4,
    v5,
    v6,
    v7,
    v8,
    v9,
    v10,
    v11,
)
from grai_source_dbt.loaders.v1 import ManifestLoaderV1
from grai_source_dbt.loaders.v7 import ManifestLoaderV7
from grai_source_dbt.utils import full_name, set_extra_fields

ManifestTypes = Union[
    v1.ManifestV1,
    v2.ManifestV2,
    v3.ManifestV3,
    v4.ManifestV4,
    v6.ManifestV6,
    v7.ManifestV7,
    v8.ManifestV8,
    v9.ManifestV9,
    v10.ManifestV10,
    v11.ManifestV11,
]
NodeTypes = Union[
    v1.NodeTypes,
    v2.NodeTypes,
    v3.NodeTypes,
    v4.NodeTypes,
    v5.NodeTypes,
    v6.NodeTypes,
    v7.NodeTypes,
    v8.NodeTypes,
    v9.NodeTypes,
    v10.NodeTypes,
    v11.NodeTypes,
]

SourceTypes = Union[
    v1.SourceTypes,
    v2.SourceTypes,
    v3.SourceTypes,
    v4.SourceTypes,
    v5.SourceTypes,
    v6.SourceTypes,
    v7.SourceTypes,
    v8.SourceTypes,
    v9.SourceTypes,
    v10.SourceTypes,
    v11.SourceTypes,
]
AllDbtNodeTypes = Union[NodeTypes, SourceTypes]
AllDbtNodeInstances = get_args(AllDbtNodeTypes)
set_extra_fields(AllDbtNodeInstances)


@full_name.register
def node_full_name(obj: NodeTypes) -> str:
    """

    Args:
        obj (NodeTypes):

    Returns:

    Raises:

    """
    return f"{obj.schema_}.{obj.name}"


@full_name.register
def source_full_name(obj: SourceTypes) -> str:
    """

    Args:
        obj (SourceTypes):

    Returns:

    Raises:

    """
    return f"{obj.schema_}.{obj.identifier}"


MANIFEST_MAP = {
    ArtifactTypes.MANIFEST_V1.value.dbt_schema_version: ManifestLoaderV1,
    ArtifactTypes.MANIFEST_V2.value.dbt_schema_version: ManifestLoaderV1,
    ArtifactTypes.MANIFEST_V3.value.dbt_schema_version: ManifestLoaderV1,
    ArtifactTypes.MANIFEST_V4.value.dbt_schema_version: ManifestLoaderV1,
    ArtifactTypes.MANIFEST_V5.value.dbt_schema_version: ManifestLoaderV1,
    ArtifactTypes.MANIFEST_V6.value.dbt_schema_version: ManifestLoaderV1,
    ArtifactTypes.MANIFEST_V7.value.dbt_schema_version: ManifestLoaderV7,
    ArtifactTypes.MANIFEST_V8.value.dbt_schema_version: ManifestLoaderV7,
    ArtifactTypes.MANIFEST_V9.value.dbt_schema_version: ManifestLoaderV7,
    ArtifactTypes.MANIFEST_V10.value.dbt_schema_version: ManifestLoaderV7,
    ArtifactTypes.MANIFEST_V11.value.dbt_schema_version: ManifestLoaderV7,
}


SUPPORTED_VERSIONS = [utils.get_schema_id_from_version(label) for label in MANIFEST_MAP.keys()]
