from __future__ import annotations
from typing import Any, Dict, List, Optional, TypeVar, Union
from pydantic import BaseModel, root_validator
from typing import TYPE_CHECKING


if TYPE_CHECKING:
    from grai_client.schemas.node import Node
    from grai_client.schemas.edge import Edge
    T = TypeVar("T", Node, Edge)


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


def merge_models(a: T, b: T) -> T:
    a_type = type(a)
    merged = merge_dicts(unpack_object(a), unpack_object(b))
    return a_type(**merged)


class GraiBaseModel(BaseModel):
    # class Config:
    #     frozen = True

    def update(self, new_values: Dict) -> BaseModel:
        values = self.dict()
        return type(self)(**merge_dicts(values, new_values))


class BaseSpec(GraiBaseModel):
    is_active: Optional[bool] = True


class PlaceHolderSchema(BaseSpec):
    @root_validator(pre=True)
    def _(cls, values):
        message = (
            "Something is wrong... I can feel it 😡. You've reached a placeholder schema - "
            "most likely the `version` of your config file doesn't exist yet."
        )
        raise AssertionError(message)



