from typing import Dict, List, Optional, TypeVar

from grai_schemas.v1 import EdgeV1, NodeV1
from grai_schemas.v1.node import NodeNamedID
from grai_schemas.utilities import merge_models
from grai_schemas.schema import GraiType

from lineage.models import Edge as EdgeModel
from lineage.models import Node as NodeModel
from workspaces.models import Workspace


def get_node(workspace: Workspace, grai_type: dict) -> NodeModel:
    if grai_type.get("id") is not None:
        return NodeModel(**grai_type)

    return NodeModel.objects.filter(workspace=workspace).get(
        namespace=grai_type.get("namespace"), name=grai_type.get("name")
    )


def deactivate(items: List[GraiType]) -> List[GraiType]:
    for item in items:
        item.spec.is_active = False

    return items


def update(
    workspace: Workspace,
    items: List[GraiType],
    active_items: Optional[List[GraiType]] = None,
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
                spec["source"] = NodeNamedID(**active_model.source.__dict__)
                spec["destination"] = NodeNamedID(**active_model.destination.__dict__)
                spec["metadata"] = {
                    "grai": {"node_type": "Edge", "edge_type": "ColumnToColumn"}
                }
            else:
                spec["metadata"] = {"grai": {"node_type": "Column"}}

            active_items.append(Schema.from_spec(spec))

    current_item_map = {hash(item.spec): item for item in active_items}
    item_map: Dict[int, GraiType] = {hash(item.spec): item for item in items}

    new_item_keys = item_map.keys() - current_item_map.keys()
    deactivated_item_keys = current_item_map.keys() - item_map.keys()
    updated_item_keys = item_map.keys() - new_item_keys

    deactivated_items = deactivate([current_item_map[k] for k in deactivated_item_keys])
    new_items: List[GraiType] = [item_map[k] for k in new_item_keys]
    updated_items = [
        merge_models(item_map[k], current_item_map[k])
        for k in updated_item_keys
        if item_map[k] != current_item_map[k]
    ]

    def schemaToModel(item: GraiType):
        values = item.spec.dict(exclude_none=True)

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
