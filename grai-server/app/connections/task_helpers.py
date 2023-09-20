import uuid
import warnings
from copy import deepcopy
from functools import singledispatch
from itertools import chain, tee
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Protocol,
    Sequence,
    Tuple,
    TypedDict,
    TypeVar,
    Union,
)
from uuid import UUID

from django.contrib.postgres.aggregates import ArrayAgg
from django.db import models
from django.db.models import Q, Value
from django.db.models.functions import Coalesce
from grai_schemas.schema import GraiType
from grai_schemas.utilities import merge
from grai_schemas.v1 import EdgeV1, NodeV1, SourcedEdgeV1, SourcedNodeV1
from grai_schemas.v1.node import NamedSpec as NodeNamedSpec
from grai_schemas.v1.node import NodeNamedID
from grai_schemas.v1.source import SourceSpec
from multimethod import multimethod
from pydantic import BaseModel

from lineage.models import Edge as EdgeModel
from lineage.models import Node as NodeModel
from lineage.models import Source
from workspaces.models import Workspace

from .adapters.schemas import model_to_schema, schema_to_model


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


def build_item_query_filter(
    from_items: List[Union[SpecNameNamespace, NameNamespace]], workspace: Union[UUID, Workspace]
):
    if len(from_items) == 0:
        raise ValueError("from_items must not be empty")

    query = Q()
    for item in from_items:
        if hasattr(item, "spec"):
            query |= Q(name=item.spec.name, namespace=item.spec.namespace)
        else:
            query |= Q(name=item.name, namespace=item.namespace)

    query &= Q(workspace=workspace)

    return query


def get_edge_nodes_from_database(items: List[SourcedEdgeV1], workspace: Workspace) -> Dict[Tuple[str, str], UUID]:
    """
    Given a list of SourcedEdgeV1, return a dictionary mapping (name, namespace) tuples to node ids for the edge
    sources and destinations. Can efficiently query for missing node_ids from the database for a collection of edges.
    """
    sources = (item.spec.source for item in items)
    destinations = (item.spec.destination for item in items)

    node_map = {}
    for item in chain(sources, destinations):
        key = (item.name, item.namespace)
        if key in node_map and node_map[key] != item.id:
            raise ValueError(f"Duplicate node label {key} with different ids {node_map[key]} and {item.id}")

        node_map[key] = item.id

    missing_node_ids = [k for k, v in node_map.items() if v is None]
    if len(missing_node_ids) == 0:
        return node_map

    query = Q()
    for name, namespace in missing_node_ids:
        query |= Q(name=name, namespace=namespace)
    query &= Q(workspace=workspace)

    node_map |= {(node.name, node.namespace): node.id for node in NodeModel.objects.filter(query).all()}

    missing_node_labels = {k for k, v in node_map.items() if v is None}
    if len(missing_node_labels) > 0:
        anomalous_edges = []
        for edge in items:
            source_id = (edge.spec.source.name, edge.spec.source.namespace)
            dest_id = (edge.spec.destination.name, edge.spec.destination.namespace)
            missing_source = source_id in missing_node_labels
            missing_dest = dest_id in missing_node_labels
            if missing_source or missing_dest:
                if missing_source and missing_dest:
                    message = "missing source and destination"
                elif missing_source:
                    message = "missing source"
                else:
                    message = "missing destination"
                anomalous_edges.append(f"{str(source_id)} -> {str(dest_id)}; {message}")

        anomalous_edge_list = "\n".join(f"- {str(edge)}" for edge in anomalous_edges[:10])
        message = (
            f"An attempt was made to create edges with missing nodes. In total there were {len(missing_node_labels)} "
            f"missing nodes corresponding to {len(anomalous_edges)} edges. "
            f"The following is a sample of {len(anomalous_edges[:10])} affected edges and the `(name, namespace)` "
            f"labels identifying their corresponding `source -> destination` nodes:\n"
            f"{anomalous_edge_list}"
        )
        raise ValueError(message)

    return node_map


def compute_graph_changes(items: List[T], active_items: List[P]) -> Tuple[List[T], List[P], List[P]]:
    current_item_map: Dict[Tuple[str, str], P] = {(item.spec.name, item.spec.namespace): item for item in active_items}
    item_map: Dict[Tuple[str, str], T] = {(item.spec.name, item.spec.namespace): item for item in items}

    updated_item_keys = item_map.keys() & current_item_map.keys()
    new_item_keys = item_map.keys() - updated_item_keys
    deactivated_item_keys = current_item_map.keys() - updated_item_keys

    new_items = [item_map[k] for k in new_item_keys]
    deactivated_items = [current_item_map[k] for k in deactivated_item_keys]
    updated_items: List[P] = [
        merge(current_item_map[k], item_map[k]) for k in updated_item_keys if item_map[k] != current_item_map[k]
    ]
    return new_items, deactivated_items, updated_items


def process_source_nodes(
    workspace: Workspace, source: Source, items: List[SourcedNodeV1], existing_nodes: Optional[List[NodeV1]] = None
) -> Tuple[List[NodeModel], List[NodeModel], List[NodeModel]]:
    if isinstance(existing_nodes, list):
        if not all(isinstance(node, NodeV1) for node in existing_nodes):
            raise ValueError(
                f"existing_nodes must be a list of NodeV1, got list of "
                f"Union[{set(type(node) for node in existing_nodes)}]"
            )
        if not all(node.spec.id for node in existing_nodes):
            raise ValueError("Some Nodes in existing_nodes are missing ids")

        active_nodes = existing_nodes
    elif existing_nodes is None:
        query = build_item_query_filter(items, workspace)
        current_item_generator = chain(NodeModel.objects.filter(query).all(), source.nodes.all())
        active_nodes = [model_to_schema(item, "NodeV1") for item in current_item_generator]
    else:
        raise ValueError("existing_nodes must be a list of NodeV1 or None")

    new_items, deactivated_items, updated_items = compute_graph_changes(items, active_nodes)

    new = [schema_to_model(item, workspace) for item in new_items]
    deactivated = [schema_to_model(item, workspace) for item in deactivated_items]
    updated = [schema_to_model(item, workspace) for item in updated_items]

    return new, deactivated, updated


def process_source_edges(
    workspace: Workspace, source: Source, items: List[SourcedEdgeV1], existing_edges: Optional[List[EdgeV1]] = None
) -> Tuple[List[EdgeModel], List[EdgeModel], List[EdgeModel]]:
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
        query = build_item_query_filter(items, workspace)
        current_item_generator = chain(EdgeModel.objects.filter(query).all(), source.edges.all())
        active_edges = [model_to_schema(item, "EdgeV1") for item in current_item_generator]
    else:
        raise ValueError("existing_edges must be a list of EdgeV1 or None")

    new_items, deactivated_items, updated_items = compute_graph_changes(items, active_edges)

    edge_map = get_edge_nodes_from_database(new_items, workspace)
    for item in new_items:
        item.spec.source.id = edge_map[(item.spec.source.name, item.spec.source.namespace)]
        item.spec.destination.id = edge_map[(item.spec.destination.name, item.spec.destination.namespace)]

    new = [schema_to_model(item, workspace) for item in new_items]
    deactivated = [schema_to_model(item, workspace) for item in deactivated_items]
    updated = [schema_to_model(item, workspace) for item in updated_items]

    return new, deactivated, updated


def process_updates(
    workspace: Workspace,
    source: Source,
    items: Optional[Union[list[SourcedNodeV1], list[SourcedEdgeV1]]] = None,
    existing_items: Optional[Union[list[NodeV1], list[EdgeV1]]] = None,
) -> Tuple[List[LineageModel], List[LineageModel], List[LineageModel]]:
    if items is None:
        return [], [], []

    item_types = {type(item) for item in items}
    if len(item_types) != 1:
        raise ValueError(f"Can't process updates for multiple item types {item_types}")

    if source.workspace != workspace:
        raise ValueError(f"Source {source} is not in workspace {workspace}")

    if isinstance(items[0], SourcedNodeV1):
        new, old, updated = process_source_nodes(workspace, source, items, existing_items)
    elif isinstance(items[0], SourcedEdgeV1):
        new, old, updated = process_source_edges(workspace, source, items, existing_items)
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

    new_items, deactivated_items, updated_items = process_updates(workspace, source, items, active_items)

    Model.objects.bulk_create(new_items)
    Model.objects.bulk_update(updated_items, ["metadata"])

    relationship.add(*new_items, *updated_items)

    if len(deactivated_items) > 0:
        relationship.remove(*deactivated_items)
        empty_source_query = Q(workspace=workspace, data_sources=None)

        deletable_nodes = NodeModel.objects.filter(empty_source_query)
        deleted_edge_query = Q(source__in=deletable_nodes) | Q(destination__in=deletable_nodes) | empty_source_query

        EdgeModel.objects.filter(deleted_edge_query).delete()
        deletable_nodes.delete()


def modelToSchema(model, Schema, type):
    spec = model.__dict__

    if type == "Edge":
        spec["source"] = NodeNamedID(**model.source.__dict__)
        spec["destination"] = NodeNamedID(**model.destination.__dict__)

    spec["data_sources"] = []

    return Schema.from_spec(spec)
