from __future__ import annotations

import uuid
from typing import (
    TYPE_CHECKING,
    Any,
    Dict,
    Generic,
    List,
    Protocol,
    Tuple,
    TypeVar,
    Union,
)

from multimethod import multimethod
from pydantic import BaseModel


class SpecProto(Protocol):
    def spec(self) -> Any:
        pass


T = TypeVar("T")


def unpack_object(obj: Union[Dict, BaseModel]) -> Dict:
    """

    Args:
        obj: The object to unpack, generally a dict or BaseModel

    Returns:

    Raises:

    """
    if isinstance(obj, Dict):
        return obj
    elif isinstance(obj, BaseModel):
        return obj.dict()
    else:
        raise NotImplementedError(f"No method to unpack objects of type {type(obj)}")


atomic = Union[int, float, complex, str, bool, uuid.UUID]


@multimethod
def merge(a, b):
    """The base merge function

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:

    Raises:

    """
    raise Exception(f"No merge logic for type {type(a)} and {type(b)}")


@merge.register
def merge_atomic(a: Any, b: T) -> T:
    """Merge an atomic value with any other value

    This function effectively handles cases where a value is being replaced.
    For example, if the value integer `5` needed to be updated to `6`, this function would handle that.

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        The new value

    Raises:

    """
    return b


@merge.register
def merge_missing(a: T, b: None) -> T:
    """Merge an object with a missing value

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        The original object

    Raises:

    """
    return a


@merge.register
def merge_dict_item(a: Dict, b: Dict) -> Dict:
    """Merge two dictionaries

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        The merged dictionary

    Raises:

    """
    result = {**a, **b}
    result.update({key: merge(a[key], b[key]) for key in a.keys() & b.keys()})
    return result


@merge.register
def merge_list(a: list, b: list) -> list:
    """Merge two lists

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        A merged list

    Raises:

    """
    return [*a, *b]


@merge.register
def merge_tuple(a: tuple, b: tuple) -> tuple:
    """Merge two tuples

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        A merged tuple

    Raises:

    """
    return *a, *b


@merge.register
def merge_set(a: set, b: set) -> set:
    """Merge two sets

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        A merged set

    Raises:

    """
    return b | a


@merge.register
def merge_pydantic(a: BaseModel, b: Any) -> BaseModel:
    """Merge a non-pydantic object into a pydantic model

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        An updated pydantic model

    Raises:

    """
    merged = merge(dict(a), b)
    return type(a)(**merged)


@merge.register
def merge_pydantic_right(a: T, b: BaseModel) -> T:
    """Merge a pydantic model into a non-pydantic model

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        An updated non-pydantic model

    Raises:

    """
    return merge(a, dict(b))


def merge_models(a: T, b: T) -> T:
    """This function is deprecated. Use `merge` instead

    Args:
        a: The first object to merge
        b: The second object to merge

    Returns:
        An updated model

    Raises:

    """
    a_type = type(a)
    merged = merge(a, b)
    return a_type(**merged)


def compute_graph_changes(
    items: List[SpecProto], active_items: List[SpecProto]
) -> Tuple[List[SpecProto], List[SpecProto], List[SpecProto]]:
    """Computes a graph update for a list of items and the corresponding set of currently active items.

    Args:
        items: The new list of graph nodes
        active_items: The current list of graph nodes. This does not have to be the full graph, only those relevant to the items set. Most commonly, these are drawn from the same data source.

    Returns:
        A three tuple of new items, updated items, and deleted items.
    Raises:

    """

    active_item_map = {hash(item.spec): item for item in active_items}
    item_map: Dict[int, SpecProto] = {hash(item.spec): item for item in items}

    new_item_keys = item_map.keys() - active_item_map.keys()
    deleted_source_item_keys = active_item_map.keys() - item_map.keys()
    updated_item_keys = item_map.keys() - new_item_keys

    deleted_from_sources = [active_item_map[k] for k in deleted_source_item_keys]

    new_items: List[SpecProto] = [item_map[k] for k in new_item_keys]
    updated_items = [item_map[k] for k in updated_item_keys if item_map[k] != active_item_map[k]]

    return new_items, updated_items, deleted_from_sources
