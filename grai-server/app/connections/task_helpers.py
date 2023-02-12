import uuid
from copy import deepcopy
from itertools import chain
from typing import Any, Dict, List, Optional, Sequence, TypeVar, Union

from django.db import models
from django.db.models import Q
from grai_schemas.schema import GraiType
from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.node import NodeNamedID
from multimethod import multimethod
from pydantic import BaseModel

from lineage.models import Edge as EdgeModel
from lineage.models import Node as NodeModel
from workspaces.models import Workspace

T = TypeVar("T")


def to_dict(instance):
    opts = instance._meta
    data = {}
    for f in chain(opts.concrete_fields, opts.private_fields):
        data[f.name] = f.value_from_object(instance)
    for f in opts.many_to_many:
        data[f.name] = [i.id for i in f.value_from_object(instance)]
    return data


atomic = Union[int, float, complex, str, bool, uuid.UUID]


@multimethod
def merge(a, b):
    raise Exception()


@merge.register
def merge_atomic(a: Any, b: Any):
    return b


@merge.register
def merge_missing(a: Any, b: None):
    return a


@merge.register
def merge_dicts(a: dict, b: dict):
    result = {**a}
    for k, v in b.items():
        result[k] = merge(result[k], v) if k in result else v

    return result


@merge.register
def merge_seq(a: list, b: list):
    return [*a, *b]


@merge.register
def merge_seq(a: tuple, b: tuple):
    return *a, *b


@merge.register
def merge_set(a: set, b: set):
    return b | a


@merge.register
def merge_node_left(a: Any, b: NodeModel):
    raise Exception()


@merge.register
def merge_node_dict(a: models.Model, b: Dict):
    assert all(hasattr(a, key) for key in b.keys()), "Can't merge dictionary into model with unknown keys"
    a_copy = deepcopy(a)
    for b_key, b_value in b.items():
        a_value = getattr(a_copy, b_key)
        setattr(a_copy, b_key, merge(a_value, b_value))
    return a_copy


@merge.register
def merge_node_node(a: models.Model, b: models.Model):
    assert isinstance(a, type(b))
    return type(a)(merge(to_dict(a), to_dict(b)))


@merge.register
def merge_pydantic(a: BaseModel, b: Any):
    merged = merge(a.dict(), b)
    return type(a)(**merged)


@merge.register
def merge_pydantic_right(a: Any, b: BaseModel):
    return merge(a, b.dict())


def get_node(workspace: Workspace, grai_type: dict) -> NodeModel:
    if grai_type.get("id") is not None:
        return NodeModel(**grai_type)

    return NodeModel.objects.filter(workspace=workspace).get(
        namespace=grai_type.get("namespace"), name=grai_type.get("name")
    )


def deactivate(items: List) -> List:
    for item in items:
        item.is_active = False

    return items


def get_existing_items(from_items, workspace, Model):
    query = Q()
    for item in from_items:
        query |= Q(name=item["name"]) & Q(namespace=item["namespace"])
        item["workspace"] = workspace

    query &= Q(workspace=workspace)
    return Model.objects.filter(query).all()


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


# def process_updates(workspace, Model, items):
#     obj_type = items[0].type
#     items = [item.spec.dict() for item in items]
#     for item in items:
#         item.pop('id', None)
#         item['workspace'] = workspace
#
#     existing_items = get_existing_items(items, workspace, Model)
#
#     current_item_map = {(item.name, item.namespace): item for item in existing_items}
#     item_map = {(item["name"], item["namespace"]): item for item in items}
#
#     new_item_keys = item_map.keys() - current_item_map.keys()
#     deactivated_item_keys = current_item_map.keys() - item_map.keys()
#     updated_item_keys = item_map.keys() - new_item_keys
#
#     for k, model in current_item_map.items():
#         item_map[k]["id"] = model.id
#
#     if obj_type == "Edge":
#
#         for k, model in current_item_map.items():
#             item_map[k]["source"] = model.source
#             item_map[k]["destination"] = model.destination
#
#         node_map = get_edge_nodes_from_database([item_map[key] for key in new_item_keys], workspace)
#
#         for key in new_item_keys:
#             source = item_map[key]["source"]
#             destination = item_map[key]["destination"]
#             item_map[key]["source"] = node_map[(source["name"], source["namespace"])]
#             item_map[key]["destination"] = node_map[(destination["name"], destination["namespace"])]
#
#     deactivated_items = deactivate([current_item_map[k] for k in deactivated_item_keys])
#
#     new_items = [Model(**item_map[k]) for k in new_item_keys]
#     for item in new_items:
#         item.set_names()
#
#
#     updated_items = (merge(current_item_map[k], item_map[k]) for k in updated_item_keys)
#     updated_items = list(updated_items)
#
#     return new_items, deactivated_items, updated_items


# def update(
#     workspace: Workspace,
#     items: List[GraiType],
# ):
#     if not items:
#         return
#     obj_type = items[0].type
#     Model = NodeModel if obj_type == "Node" else EdgeModel
#
#     new_items, deactivated_items, updated_items = process_updates(workspace, Model, items)
#
#     #Model.objects.bulk_update(deactivated_items, ["is_active"])
#     #Model.objects.bulk_update(updated_items, ["metadata"])
#     for item in updated_items:
#         item.save()
#     Model.objects.bulk_create(new_items)


def process_updates(workspace, Model, items, active_items=None):
    if not items:
        return

    type = items[0].type
    Schema = NodeV1 if type == "Node" else EdgeV1

    active_models = get_existing_items([item.spec.dict() for item in items], workspace, Model)

    if active_items is None:
        active_items = []

        for active_model in active_models:
            spec = active_model.__dict__

            if type == "Edge":
                spec["source"] = NodeNamedID(**active_model.source.__dict__)
                spec["destination"] = NodeNamedID(**active_model.destination.__dict__)

            active_items.append(Schema.from_spec(spec))

    current_item_map = {(item.spec.name, item.spec.namespace): item for item in active_items}
    item_map: Dict[int, T] = {(item.spec.name, item.spec.namespace): item for item in items}

    new_item_keys = item_map.keys() - current_item_map.keys()
    deactivated_item_keys = current_item_map.keys() - item_map.keys()
    updated_item_keys = item_map.keys() - new_item_keys

    deactivated_items = [current_item_map[k] for k in deactivated_item_keys]
    for item in deactivated_items:
        item.spec.is_active = False

    new_items = [item_map[k] for k in new_item_keys]
    updated_items = [
        merge(item_map[k], current_item_map[k]) for k in updated_item_keys if item_map[k] != current_item_map[k]
    ]

    def schemaToModel(item):
        values = item.spec.dict()
        # breakpoint()
        values["workspace"] = workspace
        # values["display_name"] = values["name"]

        if type == "Edge":
            values["source"] = get_node(workspace, values["source"])
            values["destination"] = get_node(workspace, values["destination"])

        result = Model(**values)
        result.set_names()
        return result

    new = [schemaToModel(item) for item in new_items]
    updates = [schemaToModel(item) for item in updated_items]
    deactivated_items = [schemaToModel(item) for item in deactivated_items]
    # breakpoint()
    return new, deactivated_items, updates


def update(workspace: Workspace, items: List[T], active_items: Optional[List[T]] = None):
    if not items:
        return
    Model = NodeModel if items[0].type == "Node" else EdgeModel
    new_items, deactivated_items, updated_items = process_updates(workspace, Model, items, active_items)
    # breakpoint()
    # Model.objects.bulk_update(
    #     [schemaToModel(item) for item in deactivated_items], ["is_active"]
    # )
    Model.objects.bulk_update(updated_items, ["metadata"])
    Model.objects.bulk_create(new_items)


def modelToSchema(model, Schema, type):
    spec = model.__dict__

    if type == "Edge":
        spec["source"] = NodeNamedID(**model.source.__dict__)
        spec["destination"] = NodeNamedID(**model.destination.__dict__)

    return Schema.from_spec(spec)
