from typing import Any, Dict, List, Literal, Sequence, TypeVar, Union

from grai_schemas import config as base_config
from grai_schemas.v1 import SourcedEdgeV1, SourcedNodeV1, SourceV1
from grai_schemas.v1.metadata.edges import (
    ColumnToColumnMetadata,
    EdgeMetadataTypeLabels,
    GenericEdgeMetadataV1,
    TableToColumnMetadata,
    TableToTableMetadata,
)
from grai_schemas.v1.metadata.nodes import (
    ColumnMetadata,
    NodeMetadataTypeLabels,
    TableMetadata,
)
from grai_schemas.v1.source import SourceSpec
from multimethod import multimethod

from grai_source_looker.models import Dashboard
from grai_source_looker.package_definitions import config

T = TypeVar("T")
X = TypeVar("X")
Y = TypeVar("Y")


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_grai_metadata.register
def build_grai_metadata_from_dashboard(current: Dashboard, version: Literal["v1"] = "v1") -> TableMetadata:
    """

    Args:
        current (Dashboard):
        version (Literal["v1"], optional):  (Default value = "v1")

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


@multimethod
def build_app_metadata(current: Any, desired: Any) -> None:
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)} for value {current}")


@build_app_metadata.register
def build_metadata_from_dashboard(current: Dashboard, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Dashboard):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "name": current.name,
        "display_name": current.display_name,
    }

    return data


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
def adapt_to_client(current: Any, desired: Any):
    """

    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)}")


# def make_name(node1: NodeTypes, node2: NodeTypes) -> str:
#     """

#     Args:
#         node1 (NodeTypes):
#         node2 (NodeTypes):

#     Returns:

#     Raises:

#     """
#     node1_name = f"{node1.namespace}:{node1.full_name}"
#     node2_name = f"{node2.namespace}:{node2.full_name}"
#     return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_dashboard_to_client(current: Dashboard, source: SourceSpec, version: Literal["v1"]) -> SourcedNodeV1:
    """

    Args:
        current (Dashboard):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.name,
        # "namespace": current.namespace,
        "namespace": "looker",
        "display_name": current.display_name,
        "data_source": source,
        "metadata": build_metadata(current, version),
    }
    return SourcedNodeV1.from_spec(spec_dict)


@adapt_to_client.register
def adapt_list_to_client(
    objs: List, source: SourceSpec, version: Literal["v1"]
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
