from typing import Dict, List, Optional, Tuple, TypeVar, Union

from grai_schemas.v1.edge import EdgeV1, SourcedEdgeV1
from grai_schemas.v1.node import NodeV1, SourcedNodeV1
from grai_schemas.v1.source import SourceSpec, SourceV1

from grai_client.endpoints.client import BaseClient

T = TypeVar("T", SourcedNodeV1, SourcedEdgeV1)


def compute_graph_changes(items: List[T], active_items: List[T]) -> Tuple[List[T], List[T], List[T]]:
    """
    Args:
        items:
        active_items:

    Returns:

    Raises:

    """

    active_item_map = {hash(item.spec): item for item in active_items}
    item_map: Dict[int, T] = {hash(item.spec): item for item in items}

    new_item_keys = item_map.keys() - active_item_map.keys()
    deleted_source_item_keys = active_item_map.keys() - item_map.keys()
    updated_item_keys = item_map.keys() - new_item_keys

    deleted_from_sources = [active_item_map[k] for k in deleted_source_item_keys]

    new_items: List[T] = [item_map[k] for k in new_item_keys]
    updated_items = [item_map[k] for k in updated_item_keys if item_map[k] != active_item_map[k]]

    return new_items, updated_items, deleted_from_sources


def update(
    client: BaseClient,
    items: List[Union[SourcedNodeV1, SourcedEdgeV1]],
    active_items: Optional[List[T]] = None,
    source: Optional[Union[SourceV1, SourceSpec]] = None,
):
    """

    Args:
        client:
        items:
        active_items:  (Default value = None)
        source:  (Default value = None)

    Returns:

    Raises:

    """
    if not items:
        return
    else:
        item_types = {type(item) for item in items}
        if len(item_types) != 1:
            raise ValueError(
                f"All items provided to `update` must be of the same type. Instead got a mix of types:" f" {item_types}"
            )
    if any(isinstance(item, Union[NodeV1, EdgeV1]) for item in items):
        raise NotImplementedError(
            f"Update is not supported for NodeV1 or EdgeV1. Please use SourcedNodeV1 or SourcedEdgeV1 instead."
        )
    if source is None:
        source_spec = items[0].spec.data_source
    elif isinstance(source, SourceV1):
        source_spec = source.spec
    else:
        source_spec = source

    if source_spec.id is None:
        source_spec = client.get(source_spec).spec

    sources = {item.spec.data_source for item in items}
    if len(sources) != 1:
        raise ValueError(
            f"All items provided to `update` must be from the same source. Instead got items from sources:"
            f" {sources}"
        )

    if active_items is None:
        active_items = client.get(items[0].type, source_spec.id)

    new_items, updated_items, deleted_items = compute_graph_changes(items, active_items)

    # Going to need to deal with invalid deactivated nodes.
    # new_items are valid by virtue of being created by the caller
    # updated_items should be valid by virtue of merge logic and the caller providing a valid object.
    # However, deactivated_items may be invalid if the server provided an invalid object.
    client.post(new_items)
    client.patch(updated_items)
    client.delete(deleted_items)
