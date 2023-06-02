from typing import Any, Sequence, Union

from multimethod import multimethod
from pydantic import BaseModel, Extra


@multimethod
def full_name(obj: Any) -> str:
    """

    Args:
        obj (Any):

    Returns:

    Raises:

    """
    # This is a fallback method that will be called if no other method is found
    try:
        return obj.full_name
    except AttributeError as e:
        message = (
            f"The `full_name` function requires objects to either have a `full_name` attribute or a custom "
            f"implementation for their type. No implementation was found for objects of type {type(obj)}"
        )
        raise NotImplementedError(message) from e


def set_loader_config_fields(obj: BaseModel):
    """

    Args:
        obj (BaseModel):

    Returns:

    Raises:

    """
    obj.Config.extra = Extra.allow
    obj.Config.use_enum_values = True


def set_extra_fields(obj: Union[BaseModel, Sequence[BaseModel]]) -> None:
    """

    Args:
        obj (Union[BaseModel, Sequence[BaseModel]]):

    Returns:

    Raises:

    """
    if isinstance(obj, BaseModel):
        set_loader_config_fields(obj)
    elif isinstance(obj, Sequence):
        for item in obj:
            set_loader_config_fields(item)
