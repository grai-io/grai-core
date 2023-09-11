from __future__ import annotations

import uuid
from typing import TYPE_CHECKING, Any, Dict, Generic, List, Tuple, TypeVar, Union

from multimethod import multimethod
from pydantic import BaseModel

T = TypeVar("T")


def unpack_object(obj: Union[Dict, BaseModel]) -> Dict:
    """

    Args:
        obj (Union[Dict, BaseModel]):

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
    """

    Args:
        a:
        b:

    Returns:

    Raises:

    """
    raise Exception(f"No merge logic for type {type(a)} and {type(b)}")


@merge.register
def merge_atomic(a: Any, b: T) -> T:
    """

    Args:
        a (Any):
        b (T):

    Returns:

    Raises:

    """
    return b


@merge.register
def merge_missing(a: T, b: None) -> T:
    """

    Args:
        a (T):
        b (None):

    Returns:

    Raises:

    """
    return a


@merge.register
def merge_dict_item(a: Dict, b: Dict) -> Dict:
    """

    Args:
        a (Dict):
        b (Dict):

    Returns:

    Raises:

    """
    result = {**a, **b}
    result.update({key: merge(a[key], b[key]) for key in a.keys() & b.keys()})
    return result


@merge.register
def merge_list(a: list, b: list) -> list:
    """

    Args:
        a (list):
        b (list):

    Returns:

    Raises:

    """
    return [*a, *b]


@merge.register
def merge_tuple(a: tuple, b: tuple) -> tuple:
    """

    Args:
        a (tuple):
        b (tuple):

    Returns:

    Raises:

    """
    return *a, *b


@merge.register
def merge_set(a: set, b: set) -> set:
    """

    Args:
        a (set):
        b (set):

    Returns:

    Raises:

    """
    return b | a


@merge.register
def merge_pydantic(a: BaseModel, b: Any) -> BaseModel:
    """

    Args:
        a (BaseModel):
        b (Any):

    Returns:

    Raises:

    """
    merged = merge(dict(a), b)
    return type(a)(**merged)


@merge.register
def merge_pydantic_right(a: T, b: BaseModel) -> T:
    """

    Args:
        a (T):
        b (BaseModel):

    Returns:

    Raises:

    """
    return merge(a, dict(b))


def merge_models(a: T, b: T) -> T:
    """This function is deprecated. Use `merge` instead

    Args:
        a (T):
        b (T):

    Returns:

    Raises:

    """
    a_type = type(a)
    merged = merge(a, b)
    return a_type(**merged)


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
