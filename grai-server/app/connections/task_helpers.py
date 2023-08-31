import uuid
import warnings
from copy import deepcopy
from itertools import chain
from typing import Any, Dict, List, Optional, Sequence, Tuple, TypeVar, Union, Protocol, TypedDict

from django.db import models
from django.db.models import Q
from grai_schemas.schema import GraiType
from grai_schemas.utilities import merge
from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.node import NodeNamedID, NamedSpec as NodeNamedSpec
from grai_schemas.v1.source import SourceSpec
from multimethod import multimethod
from pydantic import BaseModel

from lineage.models import Edge as EdgeModel
from lineage.models import Node as NodeModel
from lineage.models import Source
from workspaces.models import Workspace
from django.contrib.postgres.aggregates import ArrayAgg
from django.db.models.functions import Coalesce
from functools import singledispatch
from django.db.models import Value
from .adapters.schemas import schema_to_model
from uuid import UUID


class NameNamespace(Protocol):
    name: str
    namespace: str
    id: Optional[UUID]


class NameNamespaceDict(TypedDict):
    name: str
    namespace: str
    id: Optional[UUID]


class SpecNameNamespace(Protocol):
    spec: NameNamespace


T = TypeVar("T", bound=SpecNameNamespace)
P = TypeVar("P", bound=SpecNameNamespace)
LineageModel = Union[NodeModel, EdgeModel]


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


@merge.register
def merge_node_left(a: Any, b: NodeModel):
    raise Exception("Merge node left error")


@merge.register
def merge_node_dict(a: models.Model, b: Dict) -> models.Model:
    assert all(hasattr(a, key) for key in b.keys()), "Can't merge dictionary into model with unknown keys"
    a_copy = deepcopy(a)
    for b_key, b_value in b.items():
        a_value = getattr(a_copy, b_key)
        setattr(a_copy, b_key, merge(a_value, b_value))
    return a_copy


@merge.register
def merge_node_node(a: models.Model, b: models.Model) -> models.Model:
    assert isinstance(a, type(b))
    return type(a)(merge(to_dict(a), to_dict(b)))


def get_node(workspace: Workspace, grai_type: NameNamespaceDict) -> NodeModel:
    if grai_type.get("id", None) is not None:
        return NodeModel(**grai_type)

    return NodeModel.objects.filter(workspace=workspace).get(
        namespace=grai_type.get("namespace"), name=grai_type.get("name")
    )


def build_item_query_filter(from_items: List[SpecNameNamespace], workspace: Workspace):
    query = Q(workspace=workspace)
    for item in from_items:
        query |= Q(name=item.spec.name) & Q(namespace=item.spec.namespace)

    return query


def get_existing_nodes(from_items: List[Union[SourcedNodeV1, NodeV1]], workspace: Workspace) -> List[NodeV1]:
    query = build_item_query_filter(from_items, workspace)

    # The data_sources don't matter for this code path, so we don't have to fetch them from the db
    default_dict = {"data_sources": [], "workspace": workspace.id}
    return [NodeV1.from_spec({**model.__dict__, **default_dict}) for model in NodeModel.objects.filter(query).all()]


def get_existing_edges(from_items: List[Union[SourcedEdgeV1, EdgeV1]], workspace: Workspace) -> List[EdgeV1]:
    query = build_item_query_filter(from_items, workspace)

    default_dict = {"data_sources": []}
    result = []
    for item in EdgeModel.objects.filter(query).all():
        edge_dict = {**item.__dict__, **default_dict}
        edge_dict["workspace"] = edge_dict.pop("workspace_id")
        edge_dict["source"] = {"id": edge_dict.pop("source_id")}
        edge_dict["destination"] = {"id": edge_dict.pop("destination_id")}
        result.append(EdgeV1.from_spec(edge_dict))
    return result


def get_edge_nodes_from_database(items, workspace):
    sources = (item["source"] for item in items)
    destinations = (item["destination"] for item in items)
    needed_nodes = {(item["name"], item["namespace"]) for item in [*sources, *destinations]}
    query = Q()
    for name, namespace in needed_nodes:
        query |= Q(name=name) & Q(namespace=namespace)
    query &= Q(workspace=workspace)
    nodes = {(node.name, node.namespace): node for node in NodeModel.objects.filter(query).all()}
    return nodes


def compute_graph_changes(items: List[T], active_items: List[P]) -> Tuple[List[T], List[P], List[P]]:
    current_item_map: Dict[Tuple[str, str], P] = {(item.spec.name, item.spec.namespace): item for item in active_items}
    item_map: Dict[Tuple[str, str], T] = {(item.spec.name, item.spec.namespace): item for item in items}

    new_item_keys = item_map.keys() - current_item_map.keys()
    deactivated_item_keys = current_item_map.keys() - item_map.keys()
    updated_item_keys = item_map.keys() - new_item_keys

    new_items = [item_map[k] for k in new_item_keys]
    deactivated_items = [current_item_map[k] for k in deactivated_item_keys]
    updated_items: List[P] = [
        merge(current_item_map[k], item_map[k]) for k in updated_item_keys if item_map[k] != current_item_map[k]
    ]
    return new_items, deactivated_items, updated_items


def process_source_nodes(
    workspace: Workspace, items: List[SourcedNodeV1], existing_nodes: Optional[List[NodeV1]] = None
) -> Tuple[List[NodeModel], List[NodeModel], List[NodeModel]]:
    if isinstance(existing_nodes, list):
        if not all(isinstance(node, NodeV1) for node in existing_nodes):
            raise ValueError(
                f"existing_edges must be a list of NodeV1, got list of "
                f"Union[{set(type(node) for node in existing_nodes)}]"
            )
        if not all(edge.spec.id for edge in existing_nodes):
            raise ValueError("Some edges in existing_edges are missing ids")

        active_nodes = existing_nodes
    elif existing_nodes is None:
        active_nodes = get_existing_nodes(items, workspace)
    else:
        raise ValueError("existing_edges must be a list of EdgeV1 or None")

    new_items, deactivated_items, updated_items = compute_graph_changes(items, active_nodes)

    new = [schema_to_model(item, workspace) for item in new_items]
    deactivated = [schema_to_model(item, workspace) for item in deactivated_items]
    updated = [schema_to_model(item, workspace) for item in updated_items]

    return new, deactivated, updated


def process_source_edges(
    workspace: Workspace, items: List[SourcedEdgeV1], existing_edges: Optional[List[EdgeV1]] = None
) -> Tuple[List[EdgeModel], List[EdgeModel], List[EdgeModel]]:
    def build_model_from_schema(item: Union[EdgeV1, SourcedEdgeV1]) -> EdgeModel:
        values = item.spec.dict() | {"workspace": workspace}
        values["source"] = get_node(workspace, values["source"])
        values["destination"] = get_node(workspace, values["destination"])

        for key in ["data_source", "data_sources"]:
            values.pop(key, None)

        return EdgeModel(**values)

    if isinstance(existing_edges, list):
        if not all(isinstance(node, EdgeV1) for node in existing_edges):
            raise ValueError(
                f"existing_edges must be a list of EdgeV1, got list of "
                f"Union[{set(type(node) for node in existing_edges)}]"
            )
        if not all(edge.spec.id for edge in existing_edges):
            raise ValueError("Some edges in existing_edges are missing ids")

        active_edges = existing_edges
    elif existing_edges is None:
        active_edges = get_existing_edges(items, workspace)
    else:
        raise ValueError("existing_edges must be a list of EdgeV1 or None")

    new_items, deactivated_items, updated_items = compute_graph_changes(items, active_edges)
    new = [schema_to_model(item, workspace) for item in new_items]
    deactivated = [schema_to_model(item, workspace) for item in deactivated_items]
    updated = [schema_to_model(item, workspace) for item in updated_items]

    return new, deactivated, updated


def process_updates(
    workspace: Workspace,
    items: Optional[Union[list[SourcedNodeV1], list[SourcedEdgeV1]]] = None,
    existing_items: Optional[Union[list[NodeV1], list[EdgeV1]]] = None,
) -> Tuple[List[LineageModel], List[LineageModel], List[LineageModel]]:
    if not items:
        return [], [], []

    item_types = {type(item) for item in items}
    if len(item_types) != 1:
        raise ValueError(f"Can't process updates for multiple item types {item_types}")

    if isinstance(items[0], SourcedNodeV1):
        new, old, updated = process_source_nodes(workspace, items, existing_items)
    elif isinstance(items[0], SourcedEdgeV1):
        new, old, updated = process_source_edges(workspace, items, existing_items)
    else:
        raise ValueError(f"Cannot process updates for items of type {type(items[0])}")

    return new, old, updated


def update(
    workspace: Workspace,
    source: Source,
    items: List[T],
    active_items: Optional[Union[list[NodeV1], list[EdgeV1]]] = None,
):
    if not items:
        return

    item_types = items[0].type
    Model = NodeModel if item_types in ["Node", "SourceNode"] else EdgeModel
    relationship = source.nodes if item_types in ["Node", "SourceNode"] else source.edges

    new_items, deactivated_items, updated_items = process_updates(workspace, items, active_items)

    Model.objects.bulk_create(new_items)
    Model.objects.bulk_update(updated_items, ["metadata"])

    relationship.add(*new_items, *updated_items)

    if len(deactivated_items) > 0:
        relationship.remove(*deactivated_items)
        EdgeModel.objects.filter(workspace=workspace, data_sources=None).delete()
        NodeModel.objects.filter(workspace=workspace, data_sources=None).delete()


def modelToSchema(model, Schema, type):
    spec = model.__dict__

    if type == "Edge":
        spec["source"] = NodeNamedID(**model.source.__dict__)
        spec["destination"] = NodeNamedID(**model.destination.__dict__)

    spec["data_sources"] = []

    return Schema.from_spec(spec)
