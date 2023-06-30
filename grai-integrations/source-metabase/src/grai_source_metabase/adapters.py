from typing import Any, Dict, List, Literal, Union, Sequence

from grai_schemas import config as base_config
from grai_schemas.schema import Schema
from grai_schemas.v1 import NodeV1, EdgeV1
from grai_schemas.v1.metadata.edges import (
    GenericEdgeMetadataV1,
    EdgeMetadataTypeLabels,
)
from grai_schemas.v1.metadata.nodes import (
    TableMetadata,
    NodeMetadataTypeLabels,
    GenericNodeMetadataV1,
)
from multimethod import multimethod

from src.grai_source_metabase.models import Table, Question, Edge, NodeTypes
from src.grai_source_metabase.package_definitions import config


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    """
    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@build_grai_metadata.register
def build_grai_metadata_from_table(
    current: Table, version: Literal["v1"] = "v1"
) -> TableMetadata:
    """

    Args:
        current (Table):
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


@build_grai_metadata.register
def build_grai_metadata_from_question(
    current: Question, version: Literal["v1"] = "v1"
) -> GenericNodeMetadataV1:
    """

    Args:
        current (Question):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "version": version,
        "node_type": NodeMetadataTypeLabels.generic.value,
        "node_attributes": {},
        "tags": [config.metadata_id],
    }

    return GenericNodeMetadataV1(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(
    current: Edge, version: Literal["v1"] = "v1"
) -> GenericEdgeMetadataV1:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "version": version,
        "edge_type": EdgeMetadataTypeLabels.generic.value,
        "tags": [config.metadata_id],
    }

    return GenericEdgeMetadataV1(**data)


@multimethod
def build_app_metadata(current: Any, desired: Any) -> None:
    """
    Args:
        current (Any):
        desired (Any):

    Returns:

    Raises:

    """
    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@build_app_metadata.register
def build_metadata_from_table(current: Table, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Table):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    data = {
        "schema": current.schema_name,
    }

    return data


@build_app_metadata.register
def build_metadata_from_question(
    current: Question, version: Literal["v1"] = "v1"
) -> Dict:
    """

    Args:
        current (Question):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """

    return {"name": current.name}


@build_app_metadata.register
def build_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> Dict:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """

    data = {
        "definition": current.definition,
        "constraint_type": current.constraint_type.name,
    }

    data |= current.metadata if current.metadata is not None else {}

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
    base_metadata = build_grai_metadata(obj, version)
    integration_meta["grai"] = base_metadata

    return {
        base_config.metadata_id: base_metadata,
        config.metadata_id: integration_meta,
    }


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


# rewrite to check if it is question or table?


@adapt_to_client.register
def adapt_table_to_client(current: Table, version: Literal["v1"] = "v1") -> NodeV1:
    """

    Args:
        current (Table):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    # TODO: check if build_metadata has one grai key with correct values before passing it to metadata in spec_dict

    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version)["grai"],
    }

    # print("spec_dict_table", spec_dict)
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_question_to_client(
    current: Question, version: Literal["v1"] = "v1"
) -> NodeV1:
    """

    Args:
        current (Question):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """

    # TODO: check if build_metadata has one grai key with correct values before passing it to metadata in spec_dict

    spec_dict = {
        "name": current.name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version)["grai"],
    }

    # print("spec_dict_ques", spec_dict)
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: NodeTypes, node2: NodeTypes):
    """

    Args:
        node1 (NodeTypes):
        node2 (NodeTypes):

    Returns:

    Raises:

    """
    node1_fname = node1.full_name if isinstance(node1, Table) else node1.name
    node2_fname = node2.full_name if isinstance(node2, Table) else node2.name

    node1_name = f"{node1.namespace}:{node1_fname}"
    node2_name = f"{node2.namespace}:{node2_fname}"

    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_edge_to_client(current: Edge, version: Literal["v1"] = "v1") -> EdgeV1:
    """

    Args:
        current (Edge):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    # TODO: check if build_metadata has one grai key with correct values before passing it to metadata in spec_dict

    spec_dict = {
        "data_source": config.integration_name,
        "name": make_name(current.source, current.destination),
        "namespace": current.source.namespace,
        "source": {
            "name": current.source.full_name
            if isinstance(current.source, Table)
            else current.source.name,
            "namespace": current.source.namespace,
        },
        "destination": {
            "name": current.destination.full_name
            if isinstance(current.destination, Table)
            else current.destination.name,
            "namespace": current.destination.namespace,
        },
        "metadata": build_metadata(current, version)["grai"],
    }

    return Schema.to_model(spec_dict, version=version, typing_type="Edge")


@adapt_to_client.register
def adapt_seq_to_client(
    objs: Sequence, version: Literal["v1"]
) -> List[Union[NodeV1, EdgeV1]]:
    """

    Args:
        objs (Sequence):
        version (Literal["v1"]):

    Returns:

    Raises:

    """
    return [adapt_to_client(item, version) for item in objs]


@adapt_to_client.register
def adapt_list_to_client(
    objs: List, version: Literal["v1"]
) -> List[Union[NodeV1, EdgeV1]]:
    """

    Args:
        objs (List):
        version (Literal["v1"]):

    Returns:

    Raises:

    """
    return [adapt_to_client(item, version) for item in objs]
