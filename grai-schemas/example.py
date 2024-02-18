from typing import Any, Union

from multimethod import multimethod
from pydantic import BaseModel


class Meta(type):
    def __new__(cls, name, bases, dct):
        x = super().__new__(cls, name, bases, dct)
        return x


class Thing(metaclass=Meta):
    pass


class Thing2(BaseModel):
    pass


class Thing3(BaseModel):
    pass


Things = Union[Thing3, Thing2]


@multimethod
def foo(thing: Any):
    print("generic")


@foo.register
def _(thing: Things):
    print("thing or thing2")


"""
    def __new__(cls, tp, *args):
        if tp is Any:
            return object
        if hasattr(tp, '__supertype__'):  # isinstance(..., NewType) only supported >=3.10
            tp = tp.__supertype__
        if isinstance(tp, TypeVar):
            if not tp.__constraints__:
                return object
            tp = Union[tp.__constraints__]
        origin = get_origin(tp) or tp
        if hasattr(types, 'UnionType') and isinstance(tp, types.UnionType):
            origin = Union  # `|` syntax added in 3.10
        args = tuple(map(cls, get_args(tp) or args))
        if set(args) <= {object} and not (origin is tuple and args):
            return origin
        bases = (origin,) if type(origin) in (type, abc.ABCMeta) else ()
        if origin is Literal:
            bases = (subtype(Union[tuple(map(type, args))]),)
        if origin is Union:

            counts = collections.Counter(cls for arg in args for cls in get_mro(arg))
            bases = tuple(cls for cls in counts if counts[cls] == len(args))[:1]

        if origin is Callable and args[:1] == (...,):
            args = args[1:]
        namespace = {'__origin__': origin, '__args__': args}
        breakpoint()
        return type.__new__(cls, str(tp), bases, namespace)
"""
