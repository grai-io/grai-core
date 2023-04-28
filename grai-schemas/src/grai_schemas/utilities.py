from __future__ import annotations

import uuid
from typing import Any, Dict, Generic, TypeVar, Union

from multimethod import multimethod
from pydantic import BaseModel

T = TypeVar("T")


def unpack_object(obj: Union[Dict, BaseModel]) -> Dict:
    if isinstance(obj, Dict):
        return obj
    elif isinstance(obj, BaseModel):
        return obj.dict()
    else:
        raise NotImplementedError(f"No method to unpack objects of type {type(obj)}")


atomic = Union[int, float, complex, str, bool, uuid.UUID]


@multimethod
def merge(a, b):
    raise Exception()


@merge.register
def merge_atomic(a: Any, b: T) -> T:
    return b


@merge.register
def merge_missing(a: T, b: None) -> T:
    return a


@merge.register
def merge_dicts(a: dict, b: dict) -> dict:
    result = {**a}
    for k, v in b.items():
        result[k] = merge(result[k], v) if k in result else v

    return result


@merge.register
def merge_list(a: list, b: list) -> list:
    return [*a, *b]


@merge.register
def merge_tuple(a: tuple, b: tuple) -> tuple:
    return *a, *b


@merge.register
def merge_set(a: set, b: set) -> set:
    return b | a


@merge.register
def merge_pydantic(a: BaseModel, b: Any) -> BaseModel:
    merged = merge(a.dict(), b)
    return type(a)(**merged)


@merge.register
def merge_pydantic_right(a: T, b: BaseModel) -> T:
    return merge(a, b.dict())


def merge_models(a: T, b: T) -> T:
    """This function is deprecated. Use `merge` instead"""
    a_type = type(a)
    merged = merge(a, b)
    return a_type(**merged)
