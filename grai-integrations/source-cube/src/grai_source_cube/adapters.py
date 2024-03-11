from typing import Any, Dict, List, Literal, Sequence, Tuple, TypeVar, Union

from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1, SourceV1
from grai_schemas.v1.generics import SQL, Code
from grai_schemas.v1.metadata.edges import (
    EdgeMetadataTypeLabels,
    TableToColumnMetadata,
    TableToTableMetadata,
)
from grai_schemas.v1.metadata.nodes import (
    ColumnMetadata,
    NodeMetadataTypeLabels,
    TableMetadata,
)
from grai_schemas.v1.source import SourceSpec
from grai_source_cube.package_definitions import config
from grai_source_cube.types import (
    BaseCubeEdge,
    BaseNode,
    CubeEdgeColumnToColumn,
    CubeEdgeTableToColumn,
    CubeEdgeTableToTable,
    CubeEdgeTypes,
    CubeNode,
    CubeNodeTypes,
    DimensionNode,
    MeasureNode,
    SourceNode,
)
from multimethod import multimethod

T = TypeVar("T")
X = TypeVar("X")
Y = TypeVar("Y")


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    """

    Args:
        current:
        desired:

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_grai_metadata.register
def build_grai_metadata_from_dimension(current: DimensionNode, version: Literal["v1"]) -> ColumnMetadata:
    """

    Args:
        current:
        version:

    Returns:

    Raises:

    """
    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.column.value,
        "node_attributes": {
            "data_type": current.metadata.type,
            "is_primary_key": current.metadata.primaryKey,
        },
        "tags": [config.metadata_id],
    }

    return ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_measure(current: MeasureNode, version: Literal["v1"]) -> ColumnMetadata:
    """

    Args:
        current:
        version:

    Returns:

    Raises:

    """
    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.column.value,
        "node_attributes": {
            "data_type": current.metadata.type,
        },
        "tags": [config.metadata_id],
    }

    return ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_node(current: Union[CubeNode, SourceNode], version: Literal["v1"]) -> TableMetadata:
    """

    Args:
        current:
        version:

    Returns:

    Raises:

    """
    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.table.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return TableMetadata(**data)


@build_grai_metadata.register
def built_grai_metadata_from_table_to_column_edge(current: CubeEdgeTableToColumn, version: Literal["v1"]):
    data = {
        "version": version,
        "tags": [config.metadata_id],
        "edge_type": EdgeMetadataTypeLabels.table_to_column.value,
    }
    return TableToColumnMetadata(**data)


@build_grai_metadata.register
def built_grai_metadata_from_column_to_column_edge(current: CubeEdgeColumnToColumn, version: Literal["v1"]):
    data = {
        "version": version,
        "tags": [config.metadata_id],
        "edge_type": EdgeMetadataTypeLabels.table_to_column.value,
    }
    return TableToColumnMetadata(**data)


@build_grai_metadata.register
def built_grai_metadata_from_table_to_table_edge(current: CubeEdgeTableToTable, version: Literal["v1"]):
    data = {
        "version": version,
        "tags": [config.metadata_id],
        "edge_type": EdgeMetadataTypeLabels.table_to_table.value,
    }
    if isinstance(current.destination, CubeNode):
        data["code"] = Code(code=current.destination.metadata.sql, language=SQL())
    return TableToTableMetadata(**data)


@multimethod
def build_app_metadata(current: Any, desired: Any) -> None:
    """

    Args:
        current:
        desired:

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_app_metadata.register
def build_metadata_from_node(current: CubeNodeTypes, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    data = current.metadata.dict()
    return data


@build_app_metadata.register
def build_metadata_from_edge(current: CubeEdgeTypes, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    return {}


def build_metadata(obj, version):
    """

    Args:
        obj:
        version:

    Returns:

    Raises:

    """
    integration_meta = build_app_metadata(obj, version)
    integration_meta["grai"] = build_grai_metadata(obj, version)

    return integration_meta


@multimethod
def adapt_to_client():
    raise NotImplementedError("`adapt_to_client` does not have a default implementation")


@adapt_to_client.register
def unsupported_arguments(current: Any, source: Any, version: Any) -> None:
    """

    Args:
        current:
        source:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter for {type(current)} with source {type(source)} and version {type(version)}")


@adapt_to_client.register
def insufficient_arguments_2(current: Any, source: Any) -> None:
    raise NotImplementedError("Adapt to client requires three arguments: an object, a source, and a version")


@adapt_to_client.register
def insufficient_arguments_1(current: Any) -> None:
    raise NotImplementedError("Adapt to client requires three arguments: an object, a source, and a version")


@adapt_to_client.register
def adapt_source_to_client(current: SourceNode, source: SourceSpec, version: Literal["v1"]) -> SourcedNodeV1:
    """

    Args:
        current:
        source:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.node_id.name,
        "namespace": current.node_id.namespace,
        "data_source": source,
        "metadata": build_metadata(current, version),
    }
    return SourcedNodeV1.from_spec(spec_dict)


@adapt_to_client.register
def adapt_column_to_client(
    current: Union[MeasureNode, DimensionNode, CubeNode], source: SourceSpec, version: Literal["v1"]
) -> SourcedNodeV1:
    """

    Args:
        current:
        source:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.node_id.name,
        "namespace": current.node_id.namespace,
        "data_source": source,
        "metadata": build_metadata(current, version),
    }
    if current.node_id.display_name is not None:
        spec_dict["display_name"] = current.node_id.display_name
    return SourcedNodeV1.from_spec(spec_dict)


def make_name(node1: BaseNode, node2: BaseNode) -> str:
    """

    Args:
        node1:
        node2:

    Returns:

    Raises:

    """
    node1_name = f"{node1.node_id.namespace}:{node1.node_id.name}"
    node2_name = f"{node2.node_id.namespace}:{node2.node_id.name}"
    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: BaseCubeEdge, source: SourceSpec, version: Literal["v1"]) -> SourcedEdgeV1:
    """

    Args:
        current:
        source:
        version:  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "data_source": source,
        "name": make_name(current.source, current.destination),
        "namespace": current.source.node_id.namespace,
        "source": {
            "name": current.source.node_id.name,
            "namespace": current.source.node_id.namespace,
        },
        "destination": {
            "name": current.destination.node_id.name,
            "namespace": current.destination.node_id.namespace,
        },
        "metadata": build_metadata(current, version),
    }
    return SourcedEdgeV1.from_spec(spec_dict)


@adapt_to_client.register
def adapt_seq_to_client(
    objs: Union[Sequence, List, Tuple], source: SourceSpec, version: Literal["v1"]
) -> List[Union[SourcedNodeV1, SourcedEdgeV1]]:
    """

    Args:
        objs:
        source:
        version:

    Returns:

    Raises:

    """
    return [adapt_to_client(item, source, version) for item in objs]


@adapt_to_client.register
def adapt_source_spec_v1_to_client(obj: X, source: SourceV1, version: Y) -> T:
    return adapt_to_client(obj, source.spec, version)
