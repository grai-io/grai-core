from typing import Any, Dict, List, Literal, Sequence, Type, Union

import grai_schemas.models as base_schemas
from grai_client.schemas.schema import Schema
from grai_schemas import config as base_config
from grai_schemas.models import DefaultValue, GraiNodeMetadata
from multimethod import multimethod

from grai_source_flat_file.models import ID, Column, Edge, Table
from grai_source_flat_file.package_definitions import config


@multimethod
def build_grai_metadata(current: Any, desired: Any) -> None:
    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@build_grai_metadata.register
def build_grai_metadata_from_column(
    current: Column, version: Literal["v1"] = "v1"
) -> base_schemas.ColumnMetadata:
    data = {
        "version": version,
        "node_type": "Column",
        "node_attributes": {
            "data_type": current.data_type,
            "is_nullable": current.is_nullable,
        },
    }

    return base_schemas.ColumnMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_node(
    current: Table, version: Literal["v1"] = "v1"
) -> GraiNodeMetadata:
    data = {"version": version, "node_type": "Table", "node_attributes": {}}

    return base_schemas.TableMetadata(**data)


@build_grai_metadata.register
def build_grai_metadata_from_edge(
    current: Edge, version: Literal["v1"] = "v1"
) -> base_schemas.GraiEdgeMetadata:
    data = {"version": version}
    return base_schemas.GraiEdgeMetadata(**data)


@multimethod
def build_flat_file_metadata(current: Any, desired: Any) -> None:
    raise NotImplementedError(
        f"No adapter between {type(current)} and {type(desired)} for value {current}"
    )


@build_flat_file_metadata.register
def build_metadata_from_column(current: Column, version: Literal["v1"] = "v1") -> Dict:
    data = {
        "table_name": current.table,
    }
    return data


@build_flat_file_metadata.register
def build_metadata_from_edge(current: Edge, version: Literal["v1"] = "v1") -> Dict:
    data = {}
    return data


@build_flat_file_metadata.register
def build_metadata_from_node(current: Table, version: Literal["v1"] = "v1") -> Dict:
    data = {"file_name": current.file_name}
    return data


def build_metadata(obj, version):
    return {
        base_config.metadata_id: build_grai_metadata(obj, version),
        config.metadata_id: build_flat_file_metadata(obj, version),
    }


@multimethod
def adapt_to_client(current: Any, desired: Any):
    raise NotImplementedError(f"No adapter between {type(current)} and {type(desired)}")


@adapt_to_client.register
def adapt_column_to_client(
    current: Union[Table, Column], version: Literal["v1"] = "v1"
):
    spec_dict = {
        "name": current.full_name,
        "namespace": current.namespace,
        "display_name": current.name,
        "data_source": config.integration_name,
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


def make_name(node1: ID, node2: ID) -> str:
    node1_name = f"{node1.namespace}:{node1.full_name}"
    node2_name = f"{node2.namespace}:{node2.full_name}"
    return f"{node1_name} -> {node2_name}"


@adapt_to_client.register
def adapt_column_to_client(current: Edge, version: Literal["v1"] = "v1"):
    spec_dict = {
        "data_source": config.integration_name,
        "name": make_name(current.source, current.destination),
        "namespace": current.source.namespace,
        "source": {
            "name": current.source.full_name,
            "namespace": current.source.namespace,
        },
        "destination": {
            "name": current.destination.full_name,
            "namespace": current.destination.namespace,
        },
        "metadata": build_metadata(current, version),
    }
    return Schema.to_model(spec_dict, version=version, typing_type="Node")


@adapt_to_client.register
def adapt_list_to_client(objs: Sequence, version: Literal["v1"] = "v1") -> List:
    return [adapt_to_client(item, version) for item in objs]
