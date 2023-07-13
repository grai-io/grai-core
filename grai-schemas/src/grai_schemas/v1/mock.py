import datetime
import uuid

from grai_schemas.human_ids import get_human_id
from grai_schemas.v1.edge import EdgeV1
from grai_schemas.v1.edge import IDSourceSpec as EdgeIDSourceSpec
from grai_schemas.v1.edge import IDSpec as EdgeIDSpec
from grai_schemas.v1.edge import NamedSourceSpec as NamedEdgeSourceSpec
from grai_schemas.v1.edge import NamedSpec as NamedEdgeSpec
from grai_schemas.v1.edge import SourcedEdgeSpec, SourcedEdgeV1
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
from polyfactory.factories.pydantic_factory import ModelFactory


class NodeFactory(ModelFactory[NodeV1]):
    __model__ = NodeV1


class SourcedNodeFactory(ModelFactory[SourcedNodeV1]):
    __model__ = SourcedNodeV1


class NamedNodeSpecFactory(ModelFactory[NamedSpec]):
    __model__ = NamedSpec


class IDNodeSpecFactory(ModelFactory[IDSpec]):
    __model__ = IDSpec


class NamedSourceNodeSpecFactory(ModelFactory[NamedSourceSpec]):
    __model__ = NamedSourceSpec


class IDSourceNodeSpecFactory(ModelFactory[IDSourceSpec]):
    __model__ = IDSourceSpec


class MockNode:
    @classmethod
    def sourced_node(cls, **kwargs):
        """ """
        return SourcedNodeFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def node(cls, **kwargs):
        """ """
        return NodeFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def named_node_spec(self, **kwargs):
        """ """
        return NamedNodeSpecFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def id_node_spec(self, **kwargs):
        """ """
        return IDNodeSpecFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def named_source_node_spec(self, **kwargs):
        """ """
        return NamedSourceNodeSpecFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def id_source_node_spec(self, **kwargs):
        """ """
        return IDSourceNodeSpecFactory.build(factory_use_construct=True, **kwargs)


class EdgeFactory(ModelFactory[EdgeV1]):
    __model__ = EdgeV1


class SourcedEdgeFactory(ModelFactory[SourcedEdgeV1]):
    __model__ = SourcedEdgeV1


class NamedEdgeSpecFactory(ModelFactory[NamedEdgeSpec]):
    __model__ = NamedEdgeSpec


class IDEdgeSpecFactory(ModelFactory[EdgeIDSpec]):
    __model__ = EdgeIDSpec


class NamedEdgeSourceSpecFactory(ModelFactory[NamedEdgeSourceSpec]):
    __model__ = NamedEdgeSourceSpec


class IDEdgeSourceSpecFactory(ModelFactory[EdgeIDSourceSpec]):
    __model__ = EdgeIDSourceSpec


class MockEdge:
    @classmethod
    def sourced_edge(cls, **kwargs):
        """ """
        return SourcedEdgeFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def edge(cls, **kwargs):
        """ """
        return EdgeFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def named_edge_spec(cls, **kwargs):
        """ """
        return NamedEdgeSpecFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def id_edge_spec(cls, **kwargs):
        """ """
        return IDEdgeSpecFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def named_source_edge_spec(cls, **kwargs):
        """ """
        return NamedEdgeSourceSpecFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def id_source_edge_spec(cls, **kwargs):
        """ """
        return IDEdgeSourceSpecFactory.build(factory_use_construct=True, **kwargs)


class OrganisationFactory(ModelFactory[OrganisationV1]):
    __model__ = OrganisationV1


class OrganisationSpecFactory(ModelFactory[OrganisationSpec]):
    __model__ = OrganisationSpec


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


class WorkspaceFactory(ModelFactory[WorkspaceV1]):
    __model__ = WorkspaceV1


class WorkspaceSpecFactory(ModelFactory[WorkspaceSpec]):
    __model__ = WorkspaceSpec


class MockWorkspace:
    @classmethod
    def workspace(cls, **kwargs):
        """ """
        return WorkspaceFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def workspace_spec(cls, **kwargs):
        """ """
        return WorkspaceSpecFactory.build(factory_use_construct=True, **kwargs)


class SourceFactory(ModelFactory[SourceV1]):
    __model__ = SourceV1


class SourceSpecFactory(ModelFactory[SourceSpec]):
    __model__ = SourceSpec


class MockSource:
    @classmethod
    def source(cls, **kwargs):
        """ """
        return SourceFactory.build(factory_use_construct=True, **kwargs)

    @classmethod
    def source_spec(cls, **kwargs):
        """ """
        return SourceSpecFactory.build(factory_use_construct=True, **kwargs)


class MockV1:
    node = MockNode
    edge = MockEdge
    organisation = MockOrganisation
    workspace = MockWorkspace
    source = MockSource
