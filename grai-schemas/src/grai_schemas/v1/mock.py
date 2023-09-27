import datetime
import uuid
from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from grai_schemas.generics import DefaultValue
from grai_schemas.human_ids import get_human_id
from grai_schemas.v1.edge import EdgeV1
from grai_schemas.v1.edge import IDSourceSpec as EdgeIDSourceSpec
from grai_schemas.v1.edge import IDSpec as EdgeIDSpec
from grai_schemas.v1.edge import NamedSourceSpec as NamedEdgeSourceSpec
from grai_schemas.v1.edge import NamedSpec as NamedEdgeSpec
from grai_schemas.v1.edge import SourcedEdgeSpec, SourcedEdgeV1
from grai_schemas.v1.events import EventSpec, EventV1
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


class DefaultValueFactory(ModelFactory[DefaultValue]):
    __model__ = DefaultValue
    __set_as_default_factory_for_type__ = True

    has_default_value = PostGenerated(lambda name, values: values["default_value"] is not None)

    @post_generated
    @classmethod
    def data_type(cls, default_value) -> Optional[str]:
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
    """A class for generating mock nodes for testing.

    Attributes:
        workspace: The workspace to associate with the mock nodes.
        kwargs: Additional keyword arguments to pass to the factories.

    """

    def __init__(
        self,
        workspace: Optional[WorkspaceSpec] = None,
        data_source: Optional[SourceSpec] = None,
        data_sources: Optional[List[SourceSpec]] = None,
        **kwargs,
    ):
        """Initializes the MockNode class.

        Args:
            workspace: The workspace to associate with the mock nodes.
            kwargs: Additional keyword arguments to pass to the factories.
        """
        self.workspace = workspace
        self.data_source = data_source
        self.data_sources = data_sources

        self.default_spec = {}
        self.default_source_spec = {}

        if self.workspace:
            self.default_spec["workspace"] = self.workspace.id
            self.default_source_spec["workspace"] = self.workspace.id

        if self.data_source:
            self.default_source_spec["data_source"] = self.data_source

        if self.data_sources:
            self.default_spec["data_sources"] = self.data_sources

    def node(self, **kwargs) -> NodeV1:
        """Generates a mocked NodeV1 object."""
        kwargs.setdefault("spec", self.named_node_spec())
        return NodeFactory.build(**kwargs)

    def named_node_spec(self, **kwargs) -> NamedSpec:
        """Generates a mocked NamedSpec object."""
        kwargs = {**self.default_spec, **kwargs}
        base_spec = NamedNodeSpecFactory.build(**kwargs)
        return base_spec

    def id_node_spec(self, **kwargs) -> IDSpec:
        """Generates a mocked IDSpec object."""
        kwargs = {**self.default_spec, **kwargs}
        base_spec = IDNodeSpecFactory.build(**kwargs)
        return base_spec

    def sourced_node(self, **kwargs) -> SourcedNodeV1:
        """Generates a mocked SourcedNodeV1 object."""
        kwargs.setdefault("spec", self.named_source_node_spec())
        return SourcedNodeFactory.build(**kwargs)

    def named_source_node_spec(self, **kwargs) -> NamedSourceSpec:
        """Generates a mocked NamedSourceSpec object."""
        kwargs = {**self.default_source_spec, **kwargs}
        base_spec = NamedSourceNodeSpecFactory.build(**kwargs)
        return base_spec

    def id_source_node_spec(self, **kwargs) -> IDSourceSpec:
        """Generates a mocked IDSourceSpec object."""
        kwargs = {**self.default_source_spec, **kwargs}
        base_spec = IDSourceNodeSpecFactory.build(**kwargs)
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
    """A class for generating mock edges for testing.

    Attributes:
        workspace: The workspace to associate with the mock edges.
    """

    def __init__(
        self,
        workspace: Optional[WorkspaceSpec] = None,
        data_source: Optional[SourceSpec] = None,
        data_sources: Optional[List[SourceSpec]] = None,
        **kwargs,
    ):
        self.workspace = workspace
        self.data_source = data_source
        self.data_sources = data_sources

        self.default_spec = {}
        self.default_source_spec = {}

        if self.workspace:
            self.default_spec["workspace"] = self.workspace.id
            self.default_source_spec["workspace"] = self.workspace.id

        if self.data_source:
            self.default_source_spec["data_source"] = self.data_source

        if self.data_sources:
            self.default_spec["data_sources"] = self.data_sources

    def sourced_edge(self, **kwargs) -> SourcedEdgeV1:
        """Generates a mocked SourcedEdgeV1 object."""
        kwargs.setdefault("spec", self.named_source_edge_spec())
        return SourcedEdgeFactory.build(**kwargs)

    def edge(self, **kwargs) -> EdgeV1:
        """Generates a mocked EdgeV1 object."""
        kwargs.setdefault("spec", self.named_edge_spec())
        return EdgeFactory.build(**kwargs)

    def named_edge_spec(self, **kwargs) -> NamedEdgeSpec:
        """Generates a mocked NamedEdgeSpec object."""
        kwargs = {**self.default_spec, **kwargs}
        base_spec = NamedEdgeSpecFactory.build(**kwargs)

        return base_spec

    def id_edge_spec(self, **kwargs) -> EdgeIDSpec:
        """Generates a mocked EdgeIDSpec object."""
        kwargs = {**self.default_spec, **kwargs}
        base_spec = IDEdgeSpecFactory.build(**kwargs)

        return base_spec

    def named_source_edge_spec(self, **kwargs) -> NamedEdgeSourceSpec:
        """Generates a mocked NamedEdgeSourceSpec object."""
        kwargs = {**self.default_source_spec, **kwargs}
        base_spec = NamedEdgeSourceSpecFactory.build(**kwargs)

        return base_spec

    def id_source_edge_spec(self, **kwargs) -> EdgeIDSourceSpec:
        """Generates a mocked EdgeIDSourceSpec object."""
        kwargs = {**self.default_source_spec, **kwargs}
        base_spec = IDEdgeSourceSpecFactory.build(**kwargs)

        return base_spec


class OrganisationSpecFactory(ModelFactory[OrganisationSpec]):
    __model__ = OrganisationSpec
    __set_as_default_factory_for_type__ = True

    id = None
    name = get_human_id


class OrganisationFactory(ModelFactory[OrganisationV1]):
    __model__ = OrganisationV1


class MockOrganisation:
    """A class for generating mock organisations for testing."""

    @classmethod
    def organisation(cls, **kwargs) -> OrganisationV1:
        """Generate a mocked OrganisationV1 object."""
        return OrganisationFactory.build(**kwargs)

    @classmethod
    def organisation_spec(cls, **kwargs) -> OrganisationSpec:
        """Generate a mocked OrganisationSpec object."""
        return OrganisationSpecFactory.build(**kwargs)

    @classmethod
    def organization(cls, **kwargs) -> OrganisationV1:
        """Generate a mocked OrganisationV1 object."""
        return cls.organisation(**kwargs)

    @classmethod
    def organization_spec(cls, **kwargs) -> OrganisationSpec:
        """Generate a mocked OrganisationSpec object."""
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
    """A class for generating mock workspaces for testing.

    Attributes:
        organisation: The organisation to associate with the mock workspaces.
    """

    def __init__(self, organisation=None):
        """Initializes the MockWorkspace class.

        Args:
            organisation: The organisation to associate with the mock workspaces.
        """
        self.organisation = organisation

    def workspace(self, **kwargs) -> WorkspaceV1:
        """Generates a mocked WorkspaceV1 object."""
        kwargs.setdefault("spec", self.workspace_spec())
        return WorkspaceFactory.build(**kwargs)

    def workspace_spec(self, **kwargs) -> WorkspaceSpec:
        """Generates a mocked WorkspaceSpec object."""
        if self.organisation:
            kwargs.setdefault("organisation", self.organisation)
        return WorkspaceSpecFactory.build(**kwargs)


class SourceSpecFactory(ModelFactory[SourceSpec]):
    __model__ = SourceSpec
    __set_as_default_factory_for_type__ = True

    id = None
    name = get_human_id


class SourceFactory(ModelFactory[SourceV1]):
    __model__ = SourceV1


class MockSource:
    """A class for generating mocked source objects for testing.

    Attributes:
        workspace: The workspace to associate with the mock sources.
    """

    def __init__(self, workspace=None):
        """Initializes the MockSource class.

        Args:
            workspace: The workspace to associate with the mock sources.
        """
        self.workspace = workspace

        self.default_spec_kwargs = {}
        if self.workspace:
            self.default_spec_kwargs["workspace"] = self.workspace

    def source(self, **kwargs) -> SourceV1:
        """Generates a mocked SourceV1 object."""
        kwargs.setdefault("spec", self.source_spec())
        return SourceFactory.build(**kwargs)

    def source_spec(self, **kwargs) -> SourceSpec:
        """Generates a mocked SourceSpec object."""
        kwargs = {**self.default_spec_kwargs, **kwargs}
        return SourceSpecFactory.build(**kwargs)


class EventFactory(ModelFactory[EventV1]):
    __model__ = EventV1


class EventSpecFactory(ModelFactory[EventSpec]):
    __model__ = EventSpec


class MockEvent:
    """A class for generating mock events for testing.

    Attributes:
        workspace: The workspace to associate with the mock events.
    """

    def __init__(self, workspace=None):
        """Initializes the MockEvent class.

        Args:
            workspace: The workspace to associate with the mock events.
        """
        self.workspace = workspace

    def event_spec(self, **kwargs) -> EventSpec:
        """Generates a mocked EventSpec object."""
        if self.workspace:
            kwargs.setdefault("workspace", self.workspace)
        return EventSpecFactory.build(**kwargs)

    def event(self, **kwargs) -> EventV1:
        """Generates a mocked EventV1 object."""
        kwargs.setdefault("spec", self.event_spec())
        return EventFactory.build(**kwargs)


class MockV1:
    """A class for generating mock objects for testing.

    Attributes:
        node: Mocker for Node objects
        edge: Mocker for Edge objects
        organisation: Mocker for Organisation objects
        workspace: Mocker for Workspace objects
        source: Mocker for Source objects
        event: Mocker for Event objects

    """

    def __init__(
        self,
        workspace: Optional[Union[WorkspaceV1, WorkspaceSpec]] = None,
        organisation: Optional[Union[OrganisationV1, OrganisationSpec]] = None,
        data_source: Optional[Union[SourceSpec, SourceV1]] = None,
        data_sources: Optional[List[Union[SourceSpec, SourceV1]]] = None,
    ):
        """Initializes the MockV1 class.

        Args:
            workspace: The workspace to associate with the mock objects.
            organisation: The organisation to associate with the mock objects.
        """
        workspace = workspace.spec if isinstance(workspace, WorkspaceV1) else workspace
        organisation = organisation.spec if isinstance(organisation, OrganisationV1) else organisation
        data_source = data_source.spec if isinstance(data_source, SourceV1) else data_source
        if isinstance(data_sources, list):
            data_sources = [source.spec if isinstance(source, SourceV1) else source for source in data_sources]

        self.node = MockNode(workspace=workspace, data_sources=data_sources, data_source=data_source)
        self.edge = MockEdge(workspace=workspace, data_sources=data_sources, data_source=data_source)
        self.organisation = MockOrganisation
        self.workspace = MockWorkspace(organisation=organisation)
        self.source = MockSource(workspace=workspace)
        self.event = MockEvent(workspace=workspace)
