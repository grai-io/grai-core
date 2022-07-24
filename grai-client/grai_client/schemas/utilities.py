from typing import Any, Dict, List, Optional, Type, Union

from pydantic import BaseModel, root_validator


class DispatchType:
    name: str
    type: str


class BaseSpec(BaseModel):
    is_active: Optional[bool] = True


class PlaceHolderSchema(BaseSpec):
    @root_validator(pre=True)
    def _(cls, values):
        message = (
            "Something is wrong... I can feel it 😡. You've reached a placeholder schema - "
            "most likely the `version` of your config file doesn't exist yet."
        )
        raise AssertionError(message)


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
            a[k] = v
    return a


def merge_models(a: BaseModel, b: BaseModel) -> BaseModel:
    a_type = type(a)
    merged = merge_dicts(unpack_object(a), unpack_object(b))
    return a_type(**merged)
