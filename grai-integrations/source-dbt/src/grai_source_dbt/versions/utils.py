from typing import Sequence, Union

from pydantic import BaseModel, Extra


class DbtTypes:
    _nodes = []
    _all = []
    _manifests = []

    @classmethod
    def get_types(cls, objs):
        if isinstance(objs, Sequence):
            return objs
        elif isinstance(objs, type) and issubclass(objs, BaseModel):
            return [objs]
        else:
            # assumes base case is a Union
            return objs.__args__

    @classmethod
    def set_modifiers(cls, objs):
        for obj in cls.get_types(objs):
            obj.Config.extra = Extra.allow

    @classmethod
    def register_nodes(cls, objs):
        objs = cls.get_types(objs)
        cls._nodes.extend(objs)
        cls._all.extend(objs)
        cls.set_modifiers(objs)

    @classmethod
    def register_manifest(cls, objs):
        objs = cls.get_types(objs)
        cls._manifests.extend(objs)
        cls.set_modifiers(objs)

    @classmethod
    def register_all(cls, objs):
        objs = cls.get_types(objs)
        cls._all.extend(objs)
        cls.set_modifiers(objs)

    @classmethod
    @property
    def nodes(cls) -> Union:
        return Union[tuple(cls._nodes)]

    @classmethod
    @property
    def all(cls) -> Union:
        return Union[tuple(cls._all)]

    @classmethod
    @property
    def manifests(cls) -> Union:
        return Union[tuple(cls._manifests)]


class GraiExtras(BaseModel):
    namespace: str
    full_name: str
