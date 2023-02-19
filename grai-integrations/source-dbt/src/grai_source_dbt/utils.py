from multimethod import multimethod


@multimethod
def full_name(obj) -> str:
    return obj.full_name
