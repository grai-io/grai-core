from typing import Dict, List, Optional, TypeVar

from grai_client.schemas.edge import Edge, EdgeV1
from grai_client.schemas.node import Node, NodeID, NodeV1
from grai_client.schemas.utilities import merge_models
from lineage.models import Edge as EdgeModel
from lineage.models import Node as NodeModel
from workspaces.models import Workspace

T = TypeVar("T", Node, Edge)


def get_node(workspace: Workspace, grai_type: NodeID) -> NodeModel:
    if grai_type.id is not None:
        return NodeModel(**grai_type.__dict__)

    return NodeModel.objects.filter(workspace=workspace).get(
        namespace=grai_type.namespace, name=grai_type.name
    )


def deactivate(items: List[T]) -> List[T]:
    for item in items:
        item.spec.is_active = False

    return items


def update(
    workspace: Workspace,
    items: List[T],
    active_items: Optional[List[T]] = None,
):
    if not items:
        return

    type = items[0].type
    Model = NodeModel if type == "Node" else EdgeModel
    Schema = NodeV1 if type == "Node" else EdgeV1

    if active_items is None:
        active_models = Model.objects.filter(workspace=workspace).all()

        active_items = []

        for active_model in active_models:
            spec = active_model.__dict__

            if type == "Edge":
                spec["source"] = NodeID(**active_model.source.__dict__)
                spec["destination"] = NodeID(**active_model.destination.__dict__)

            active_items.append(Schema.from_spec(spec))

    current_item_map = {hash(item.spec): item for item in active_items}
    item_map: Dict[int, T] = {hash(item.spec): item for item in items}

    new_item_keys = item_map.keys() - current_item_map.keys()
    deactivated_item_keys = current_item_map.keys() - item_map.keys()
    updated_item_keys = item_map.keys() - new_item_keys

    deactivated_items = deactivate([current_item_map[k] for k in deactivated_item_keys])
    new_items: List[T] = [item_map[k] for k in new_item_keys]
    updated_items = [
        merge_models(item_map[k], current_item_map[k])
        for k in updated_item_keys
        if item_map[k] != current_item_map[k]
    ]

    def schemaToModel(item: T):
        values = item.spec.__dict__

        values["workspace"] = workspace
        values["display_name"] = values["name"]

        if type == "Edge":
            values["source"] = get_node(workspace, values["source"])
            values["destination"] = get_node(workspace, values["destination"])

        return Model(**values)

    Model.objects.bulk_update(
        [schemaToModel(item) for item in deactivated_items], ["is_active"]
    )
    Model.objects.bulk_update(
        [schemaToModel(item) for item in updated_items], ["metadata"]
    )
    Model.objects.bulk_create([schemaToModel(item) for item in new_items])
