from abc import ABC, abstractmethod

from pydantic import BaseModel

from grai_source_dbt.utils import full_name
from grai_source_dbt.versions.utils import DbtTypes, GraiExtras


class BaseManifestLoader(ABC):
    def __init__(self, manifest: BaseModel, namespace: str, *args, **kwargs):
        self.manifest = manifest
        self.namespace = namespace

        for node in self.manifest.nodes.values():
            node.grai_ = GraiExtras(full_name=full_name(node), namespace=self.namespace)
        for node in self.manifest.sources.values():
            node.grai_ = GraiExtras(full_name=full_name(node), namespace=self.namespace)

    @property
    @abstractmethod
    def nodes(self):
        raise NotImplementedError

    @property
    @abstractmethod
    def edges(self):
        raise NotImplementedError
