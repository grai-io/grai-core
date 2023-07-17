import datetime
import uuid
from typing import Any, Dict, Generic, List, Type, TypeVar

from grai_schemas.generics import DefaultValue
from grai_schemas.human_ids import get_human_id
from grai_schemas.v1.edge import EdgeV1
from grai_schemas.v1.edge import IDSourceSpec as EdgeIDSourceSpec
from grai_schemas.v1.edge import IDSpec as EdgeIDSpec
from grai_schemas.v1.edge import NamedSourceSpec as NamedEdgeSourceSpec
from grai_schemas.v1.edge import NamedSpec as NamedEdgeSpec
from grai_schemas.v1.edge import SourcedEdgeSpec, SourcedEdgeV1
from grai_schemas.v1.metadata import edges, nodes
from grai_schemas.v1.metadata.metadata import (
    EdgeMetadataV1,
    GraiEdgeMetadataV1,
    GraiNodeMetadataV1,
    NodeMetadataV1,
    SourcesEdgeMetadataV1,
    SourcesNodeMetadataV1,
)
from grai_schemas.v1.node import (
    IDSourceSpec,
    IDSpec,
    NamedSourceSpec,
    NamedSpec,
    NodeV1,
    SourcedNodeSpec,
    SourcedNodeV1,
)
from grai_schemas.v1.organization import OrganisationSpec, OrganisationV1
from grai_schemas.v1.source import SourceSpec, SourceV1
from grai_schemas.v1.workspace import WorkspaceSpec, WorkspaceV1
from polyfactory import Ignore, PostGenerated
from polyfactory.decorators import post_generated
from polyfactory.factories.pydantic_factory import ModelFactory

T = TypeVar("T")


# class MetadataFactory(ModelFactory[MetadataV1]):
#     __model__ = MetadataV1
#     __set_as_default_factory_for_type__ = True
#
#     @post_generated
#     @classmethod
#     def sources(cls, grai) -> Dict[str, GraiMetadataV1]:
#


class DefaultValueFactory(ModelFactory[DefaultValue]):
    __model__ = DefaultValue
    __set_as_default_factory_for_type__ = True

    has_default_value = PostGenerated(lambda name, values: values["default_value"] is not None)

    @post_generated
    @classmethod
    def data_type(cls, default_value) -> str:
        """ """
        return None if default_value is None else type(default_value).__name__


class GraiNodeMetadataV1Factory(ModelFactory[GraiNodeMetadataV1]):
    __model__ = GraiNodeMetadataV1
    __set_as_default_factory_for_type__ = True


class GraiEdgeMetadataV1Factory(ModelFactory[GraiEdgeMetadataV1]):
    __model__ = GraiEdgeMetadataV1
    __set_as_default_factory_for_type__ = True


class SourcesNodeMetadataV1Factory(ModelFactory[SourcesNodeMetadataV1]):
    __model__ = SourcesNodeMetadataV1
    __set_as_default_factory_for_type__ = True


class SourcesEdgeMetadataV1Factory(ModelFactory[SourcesEdgeMetadataV1]):
    __model__ = SourcesEdgeMetadataV1
    __set_as_default_factory_for_type__ = True


class NodeMetadataV1Factory(ModelFactory[NodeMetadataV1]):
    __model__ = NodeMetadataV1
    __set_as_default_factory_for_type__ = True


class EdgeMetadataV1Factory(ModelFactory[EdgeMetadataV1]):
    __model__ = EdgeMetadataV1
    __set_as_default_factory_for_type__ = True


class NamedNodeSpecFactory(ModelFactory[NamedSpec]):
    __set_as_default_factory_for_type__ = True
    __model__ = NamedSpec

    id = None
    name = get_human_id
    namespace = get_human_id
    data_sources = lambda: [SourceSpecFactory.build()]

    @post_generated
    @classmethod
    def metadata(cls, data_sources: List[SourceSpec]) -> NodeMetadataV1:
        """ """
        sources = {source.name: GraiNodeMetadataV1Factory.build() for source in data_sources}
        return NodeMetadataV1Factory.build(sources=sources)

    @post_generated
    @classmethod
    def is_active(cls, data_sources: List[SourceSpec]) -> bool:
        """ """
        return len(data_sources) > 0


class IDNodeSpecFactory(ModelFactory[IDSpec]):
    __set_as_default_factory_for_type__ = True
    __model__ = IDSpec


class NodeFactory(ModelFactory[NodeV1]):
    __model__ = NodeV1

    __set_as_default_factory_for_type__ = True
    spec = NamedNodeSpecFactory.build


class NamedSourceNodeSpecFactory(ModelFactory[NamedSourceSpec]):
    __model__ = NamedSourceSpec

    id = None
    name = get_human_id
    namespace = get_human_id


class IDSourceNodeSpecFactory(ModelFactory[IDSourceSpec]):
    __model__ = IDSourceSpec


class SourcedNodeFactory(ModelFactory[SourcedNodeV1]):
    __model__ = SourcedNodeV1

    __set_as_default_factory_for_type__ = True
    spec = NamedSourceNodeSpecFactory.build


class MockNode:
    def __init__(self, workspace=None, **kwargs):
        self.workspace = workspace
        self.kwargs = kwargs

    def node(self, **kwargs):
        """ """
        kwargs.setdefault("spec", self.named_node_spec())
        return NodeFactory.build(factory_use_construct=True, **kwargs)

    def named_node_spec(self, **kwargs):
        """ """
        base_spec = NamedNodeSpecFactory.build(factory_use_construct=True, **kwargs)
        if self.workspace:
            base_spec.workspace = self.workspace.id
        return base_spec

    def id_node_spec(self, **kwargs):
        """ """
        base_spec = IDNodeSpecFactory.build(factory_use_construct=True, **kwargs)
        if self.workspace:
            base_spec.workspace = self.workspace.id
        return base_spec

    def sourced_node(self, **kwargs):
        """ """
        kwargs.setdefault("spec", self.named_source_node_spec())
        return SourcedNodeFactory.build(factory_use_construct=True, **kwargs)

    def named_source_node_spec(self, **kwargs):
        """ """
        base_spec = NamedSourceNodeSpecFactory.build(factory_use_construct=True, **kwargs)

        if self.workspace:
            base_spec.workspace = self.workspace.id
        return base_spec

    def id_source_node_spec(self, **kwargs):
        """ """
        base_spec = IDSourceNodeSpecFactory.build(factory_use_construct=True, **kwargs)

        if self.workspace:
            base_spec.workspace = self.workspace.id
        return base_spec


class NamedEdgeSpecFactory(ModelFactory[NamedEdgeSpec]):
    __model__ = NamedEdgeSpec
    __set_as_default_factory_for_type__ = True

    id = None
    data_sources = lambda: [SourceSpecFactory.build()]

    @post_generated
    @classmethod
    def metadata(cls, data_sources: List[SourceSpec]) -> EdgeMetadataV1:
        """ """
        sources = {source.name: GraiEdgeMetadataV1Factory.build() for source in data_sources}
        return EdgeMetadataV1Factory.build(sources=sources)

    @post_generated
    @classmethod
    def is_active(cls, data_sources: List[SourceSpec]) -> bool:
        """ """
        return len(data_sources) > 0


class IDEdgeSpecFactory(ModelFactory[EdgeIDSpec]):
    __model__ = EdgeIDSpec


class EdgeFactory(ModelFactory[EdgeV1]):
    __model__ = EdgeV1

    __set_as_default_factory_for_type__ = True
    spec = NamedEdgeSpecFactory.build


class NamedEdgeSourceSpecFactory(ModelFactory[NamedEdgeSourceSpec]):
    __model__ = NamedEdgeSourceSpec
    __set_as_default_factory_for_type__ = True

    id = None


class IDEdgeSourceSpecFactory(ModelFactory[EdgeIDSourceSpec]):
    __model__ = EdgeIDSourceSpec


class SourcedEdgeFactory(ModelFactory[SourcedEdgeV1]):
    __model__ = SourcedEdgeV1

    __set_as_default_factory_for_type__ = True
    spec = NamedEdgeSourceSpecFactory.build


class MockEdge:
    def __init__(self, workspace=None, **kwargs):
        self.workspace = workspace

    def sourced_edge(self, **kwargs):
        """ """
        kwargs.setdefault("spec", self.named_source_edge_spec())
        return SourcedEdgeFactory.build(factory_use_construct=True, **kwargs)

    def edge(self, **kwargs):
        """ """
        kwargs.setdefault("spec", self.named_edge_spec())
        return EdgeFactory.build(factory_use_construct=True, **kwargs)

    def named_edge_spec(self, **kwargs):
        """ """
        base_spec = NamedEdgeSpecFactory.build(factory_use_construct=True, **kwargs)

        if self.workspace:
            base_spec.workspace = self.workspace.id

        return base_spec

    def id_edge_spec(self, **kwargs):
        """ """
        base_spec = IDEdgeSpecFactory.build(factory_use_construct=True, **kwargs)

        if self.workspace:
            base_spec.workspace = self.workspace.id

        return base_spec

    def named_source_edge_spec(self, **kwargs):
        """ """
        base_spec = NamedEdgeSourceSpecFactory.build(factory_use_construct=True, **kwargs)

        if self.workspace:
            base_spec.workspace = self.workspace.id

        return base_spec

    def id_source_edge_spec(self, **kwargs):
        """ """
        base_spec = IDEdgeSourceSpecFactory.build(factory_use_construct=True, **kwargs)

        if self.workspace:
            base_spec.workspace = self.workspace.id

        return base_spec


class OrganisationSpecFactory(ModelFactory[OrganisationSpec]):
    __model__ = OrganisationSpec
    __set_as_default_factory_for_type__ = True

    id = None
    name = get_human_id


class OrganisationFactory(ModelFactory[OrganisationV1]):
    __model__ = OrganisationV1


class MockOrganisation:
    @classmethod
    def organisation(cls, **kwargs):
        """ """
        return OrganisationFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def organisation_spec(cls, **kwargs):
        """ """
        return OrganisationSpecFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def organization(cls, **kwargs):
        """ """
        return cls.organisation(**kwargs)

    @classmethod
    def organization_spec(cls, **kwargs):
        """ """
        return cls.organisation_spec(**kwargs)


class WorkspaceSpecFactory(ModelFactory[WorkspaceSpec]):
    __model__ = WorkspaceSpec
    __set_as_default_factory_for_type__ = True

    id = None
    name = get_human_id
    organisation = OrganisationSpecFactory.build

    @post_generated
    @classmethod
    def ref(cls, name, organisation) -> str:
        """ """
        return f"{organisation.name}/{name}"


class WorkspaceFactory(ModelFactory[WorkspaceV1]):
    __model__ = WorkspaceV1


class MockWorkspace:
    def __init__(self, organisation=None):
        self.organisation = organisation

    def workspace(self, **kwargs):
        """ """
        kwargs.setdefault("spec", self.workspace_spec())
        return WorkspaceFactory.build(factory_use_construct=True, **kwargs)

    def workspace_spec(self, **kwargs):
        """ """
        if self.organisation:
            kwargs.setdefault("organisation", self.organisation)
        return WorkspaceSpecFactory.build(factory_use_construct=True, **kwargs)


class SourceSpecFactory(ModelFactory[SourceSpec]):
    __model__ = SourceSpec
    __set_as_default_factory_for_type__ = True

    id = None
    name = get_human_id


class SourceFactory(ModelFactory[SourceV1]):
    __model__ = SourceV1


class MockSource:
    def __init__(self, workspace=None):
        self.workspace = workspace

    def source(self, **kwargs):
        """ """
        kwargs.setdefault("spec", self.source_spec())
        return SourceFactory.build(factory_use_construct=True, **kwargs)

    def source_spec(self, **kwargs):
        """ """
        if self.workspace:
            kwargs.setdefault("workspace", self.workspace)
        return SourceSpecFactory.build(factory_use_construct=True, **kwargs)


class MockV1:
    def __init__(self, workspace=None, organisation=None):
        workspace = workspace.spec if isinstance(workspace, WorkspaceV1) else workspace
        organisation = organisation.spec if isinstance(organisation, OrganisationV1) else organisation

        self.node = MockNode(workspace=workspace)
        self.edge = MockEdge(workspace=workspace)
        self.organisation = MockOrganisation
        self.workspace = MockWorkspace(organisation=organisation)
        self.source = MockSource(workspace=workspace)
