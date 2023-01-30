from __future__ import annotations

from typing import Dict, TypeVar, Union

from pydantic import BaseModel

T = TypeVar("T")


def unpack_object(obj: Union[Dict, BaseModel]) -> Dict:
    if isinstance(obj, Dict):
        return obj
    elif isinstance(obj, BaseModel):
        return obj.dict()
    else:
        raise NotImplementedError(f"No method to unpack objects of type {type(obj)}")


def merge_dicts(a: Dict, b: Dict) -> Dict:
    for k, v in b.items():
        if isinstance(a.get(k, None), dict) and isinstance(v, dict):
            merge_dicts(a[k], v)
        else:
            if v is not None:
                a[k] = v
    return a


def merge_models(a: T, b: T) -> T:
    a_type = type(a)
    merged = merge_dicts(unpack_object(a), unpack_object(b))
    return a_type(**merged)
