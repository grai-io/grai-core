from typing import Dict, List, Optional, TypeVar

from grai_schemas.base import Edge, Node
from grai_schemas.utilities import merge, merge_models

from grai_client.endpoints.client import BaseClient

T = TypeVar("T", Node, Edge)


def deactivate(items: List[T]) -> List[T]:
    updated = [item.update({"spec": {"is_active": False}}) for item in items]
    return updated  # type: ignore


def update(client: BaseClient, items: List[T], active_items: Optional[List[T]] = None):
    if not items:
        return

    if active_items is None:
        active_items = client.get(items[0].type)
        if active_items is None:
            active_items = []

    current_item_map = {hash(item.spec): item for item in active_items}
    item_map: Dict[int, T] = {hash(item.spec): item for item in items}

    new_item_keys = item_map.keys() - current_item_map.keys()
    deactivated_item_keys = current_item_map.keys() - item_map.keys()
    updated_item_keys = item_map.keys() - new_item_keys

    deactivated_items = deactivate([current_item_map[k] for k in deactivated_item_keys])
    new_items: List[T] = [item_map[k] for k in new_item_keys]
    updated_items = [
        merge(item_map[k], current_item_map[k]) for k in updated_item_keys if item_map[k] != current_item_map[k]
    ]
    # client.patch(deactivated_items)
    client.patch(updated_items)
    client.post(new_items)
