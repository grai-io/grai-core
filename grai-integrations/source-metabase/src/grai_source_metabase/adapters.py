from typing import Any, Dict, List, Literal, Union, Sequence

from grai_schemas import config as base_config
from grai_schemas.schema import Schema
from grai_schemas.v1 import NodeV1, EdgeV1
from grai_schemas.v1.metadata.nodes import (
    TableMetadata,
    NodeMetadataTypeLabels,
    GenericNodeMetadataV1,
)
from multimethod import multimethod

from models import Table, Question
from package_definitions import config


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
def build_app_method_from_table(
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
        "schema": current.schema,
    }

    return TableMetadata(**data)


@build_app_metadata.register
def build_app_method_from_question(
    current: Question, version: Literal["v1"] = "v1"
) -> Dict:
    """

    Args:
        current (Question):
        version (Literal["v1"], optional):  (Default value = "v1")

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


@adapt_to_client.register
def adapt_table_to_client(current: Table, version: Literal["v1"] = "v1") -> NodeV1:
    """

    Args:
        current (Table):
        version (Literal["v1"], optional):  (Default value = "v1")

    Returns:

    Raises:

    """
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


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
