from multimethod import multimethod


@multimethod
def full_name(obj) -> str:
    # This is a fallback method that will be called if no other method is found
    try:
        return obj.full_name
    except AttributeError as e:
        message = (
            f"The `full_name` function requires objects to either have a `full_name` attribute or a custom "
            f"implementation for their type. No implementation was found for objects of type {type(obj)}"
        )
        raise NotImplementedError(message) from e
