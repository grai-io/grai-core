from copy import deepcopy
from typing import Dict, List

from django.db.models import Q
from grai_schemas.schema import GraiType

from lineage.models import Edge as EdgeModel
from lineage.models import Node as NodeModel
from workspaces.models import Workspace


def merge_dicts(a: Dict, b: Dict) -> Dict:
    for k, v in b.items():
        if isinstance(a.get(k, None), dict) and isinstance(v, dict):
            merge_dicts(a[k], v)
        else:
            if v is not None:
                a[k] = v
    return a


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


def process_updates(workspace, Model, items):
    obj_type = items[0].type
    items = [item.spec.dict() for item in items]
    existing_items = get_existing_items(items, workspace, Model)

    current_item_map = {(item.name, item.namespace): item for item in existing_items}
    item_map = {(item["name"], item["namespace"]): item for item in items}

    new_item_keys = item_map.keys() - current_item_map.keys()
    deactivated_item_keys = current_item_map.keys() - item_map.keys()
    updated_item_keys = item_map.keys() - new_item_keys

    for k, model in current_item_map.items():
        item_map[k]["id"] = model.id

    if obj_type == "Edge":

        for k, model in current_item_map.items():
            item_map[k]["source"] = model.source
            item_map[k]["destination"] = model.destination

        node_map = get_edge_nodes_from_database([item_map[key] for key in new_item_keys], workspace)

        for key in new_item_keys:
            source = item_map[key]["source"]
            destination = item_map[key]["destination"]
            item_map[key]["source"] = node_map[(source["name"], source["namespace"])]
            item_map[key]["destination"] = node_map[(destination["name"], destination["namespace"])]

    deactivated_items = deactivate([current_item_map[k] for k in deactivated_item_keys])

    new_items = [item_map[k] for k in new_item_keys]
    for item in new_items:
        item.pop("id", None)
    new_items = [Model(**item) for item in new_items]
    for item in new_items:
        item.set_names()

    updated_items = []
    for k in updated_item_keys:
        current_item = deepcopy(current_item_map[k])

        for item_key, item_value in item_map[k].items():
            if isinstance(item_value, dict):
                if "new_thing" in item_value["grai"] or "new_thing" in current_item.metadata["grai"]:
                    breakpoint()
                merged_value = merge_dicts(getattr(current_item, item_key), item_value)
                setattr(current_item, item_key, merged_value)

            # elif item_value != getattr(current_item, item_key) and item_value is not None:
            elif item_value is not None:
                setattr(current_item, item_key, item_value)
        updated_items.append(current_item)
        # if current_item != current_item_map[k]:
        #     updated_items.append(current_item)
    return new_items, deactivated_items, updated_items


def update(
    workspace: Workspace,
    items: List[GraiType],
):
    if not items:
        return
    obj_type = items[0].type
    Model = NodeModel if obj_type == "Node" else EdgeModel

    new_items, updated_items, deactivated_items = process_updates(workspace, Model, items)

    Model.objects.bulk_update(deactivated_items, ["is_active"])
    Model.objects.bulk_update(updated_items, ["metadata"])
    Model.objects.bulk_create(new_items)
