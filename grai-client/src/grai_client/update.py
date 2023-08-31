from typing import Dict, List, Optional, Tuple, TypeVar, Union

from grai_schemas.utilities import compute_graph_changes
from grai_schemas.v1.edge import EdgeV1, SourcedEdgeV1
from grai_schemas.v1.node import NodeV1, SourcedNodeV1
from grai_schemas.v1.source import SourceSpec, SourceV1

from grai_client.endpoints.client import BaseClient

T = TypeVar("T", SourcedNodeV1, SourcedEdgeV1)


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
    if any(isinstance(item, (NodeV1, EdgeV1)) for item in items):
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
