import pprint
from typing import Any, List, Literal, Optional, Sequence, Type, TypeVar
from uuid import UUID

from django.db.models import Q
from django.db.models.query import QuerySet
from grai_schemas.v1.edge import EdgeSpec, EdgeV1, SourcedEdgeSpec, SourcedEdgeV1
from grai_schemas.v1.node import (
    NodeNamedID,
    NodeSpec,
    NodeV1,
    SourcedNodeSpec,
    SourcedNodeV1,
)
from grai_schemas.v1.organization import OrganisationSpec, OrganisationV1
from grai_schemas.v1.source import SourceSpec, SourceV1
from grai_schemas.v1.workspace import WorkspaceSpec, WorkspaceV1
from multimethod import multimethod

from lineage.models import Edge, Node, Source
from workspaces.models import Organisation, Workspace

T = TypeVar("T")
R = TypeVar("R")


def get_data_source_models(data_sources: Sequence[SourceSpec], workspace: Workspace) -> List[Source]:
    uuids = [source_id for source_id in data_sources if isinstance(source_id, UUID)]
    uuid_sources = Source.objects.filter(workspace=workspace, id__in=uuids).all()
    if missing_uuids := set(uuids) - set(model.id for model in uuid_sources):
        raise ValueError(
            f"Some of the provided source ids do not exist in the database. Please insure the following source ids"
            f"have been created in the database: \n"
            f"{pprint.pprint(list(missing_uuids))}"
        )

    source_model_gen = (node_source for node_source in data_sources if isinstance(node_source, SourceSpec))
    source_models = [source_v1_spec_to_model(node_source, workspace=workspace) for node_source in source_model_gen]
    return [*uuid_sources, *source_models]


def organization_v1_spec_to_model(organization: OrganisationSpec) -> Organisation:
    raise NotImplementedError()


def organization_v1_to_model(organization: OrganisationV1) -> Organisation:
    return organization_v1_spec_to_model(organization.spec)


def workspace_v1_spec_to_model(workspace_arg: WorkspaceSpec) -> Workspace:
    raise NotImplementedError()


def workspace_v1_to_model(workspace_arg: WorkspaceV1) -> Workspace:
    return workspace_v1_spec_to_model(workspace_arg.spec)


def source_v1_spec_to_model(source: SourceSpec, workspace: Workspace) -> Source:
    return Source(name=source.name, workspace=workspace)


def source_v1_to_model(source: SourceV1, workspace: Workspace) -> Source:
    return source_v1_spec_to_model(source.spec, workspace)


def source_node_v1_spec_to_model(source_node: SourcedNodeSpec, workspace: Workspace) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return node_v1_spec_to_model(source_node.to_node(), workspace)


def source_node_v1_to_model(source_node: SourcedNodeV1, workspace: Workspace) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return source_node_v1_spec_to_model(source_node.spec, workspace)


def node_v1_spec_to_model(node: NodeSpec, workspace: Workspace) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    values = node.dict(exclude={"data_sources", "workspace"}) | {"workspace": workspace}

    result = Node(**values)
    result.set_names()

    return result


def node_v1_to_model(node: NodeV1, workspace: Workspace) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return node_v1_spec_to_model(node.spec, workspace)


def source_edge_v1_spec_to_model(source_edge: SourcedEdgeSpec, workspace: Workspace) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return edge_v1_spec_to_model(source_edge.to_edge(), workspace)


def source_edge_v1_to_model(source_edge: SourcedEdgeV1, workspace: Workspace) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return source_edge_v1_spec_to_model(source_edge.spec, workspace)


def edge_v1_spec_to_model(edge: EdgeSpec, workspace: Workspace) -> Edge:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    values = edge.dict(exclude={"workspace", "data_sources"}) | {"workspace": workspace}

    if edge.source.id is None or edge.destination.id is None:
        source_name = Q(name=edge.source.name, namespace=edge.source.namespace)
        destination_name = Q(name=edge.destination.name, namespace=edge.destination.namespace)
        workspace_filter = Q(workspace=workspace)
        query = (source_name | destination_name) & workspace_filter

        nodes = Node.objects.filter(query).all()
        if len(nodes) != 2:
            found_nodes = "\n".join([f"- (name={n.name} & namespace={n.namespace})" for n in nodes])
            message = (
                f"Could not find the source and destination nodes for edge: "
                f"(name={edge.name}, namespace={edge.namespace}) in workspace={workspace}. "
                f"We were expecting to find 2 nodes but only found {len(nodes)}. "
                f"\n\nReturned nodes include:\n{found_nodes}"
            )
            raise ValueError(message)
        source, destination = nodes
        if source.name != edge.source.name or source.namespace != edge.source.namespace:
            destination, source = source, destination
    else:
        source = Node(**edge.source.dict(exclude={"namespace"}))
        destination = Node(**edge.destination.dict(exclude={"namespace"}))

    values["source"] = source
    values["destination"] = destination

    result = Edge(**values)
    result.set_names()

    return result


def edge_v1_to_model(edge: EdgeV1, workspace: Workspace) -> Edge:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return edge_v1_spec_to_model(edge.spec, workspace)


def schema_to_model(item: Any, workspace: Optional[Workspace] = None):
    if isinstance(item, NodeV1):
        return node_v1_to_model(item, workspace)
    elif isinstance(item, NodeSpec):
        return node_v1_spec_to_model(item, workspace)
    elif isinstance(item, EdgeSpec):
        return edge_v1_spec_to_model(item, workspace)
    elif isinstance(item, EdgeV1):
        return edge_v1_to_model(item, workspace)
    elif isinstance(item, SourceSpec):
        return source_v1_spec_to_model(item, workspace)
    elif isinstance(item, SourceV1):
        return source_v1_to_model(item, workspace)
    elif isinstance(item, WorkspaceV1):
        return workspace_v1_to_model(item, workspace)
    elif isinstance(item, WorkspaceSpec):
        return workspace_v1_spec_to_model(item, workspace)
    elif isinstance(item, OrganisationSpec):
        return organization_v1_spec_to_model(item)
    elif isinstance(item, OrganisationV1):
        return organization_v1_to_model(item)
    elif isinstance(item, SourcedEdgeV1):
        return source_edge_v1_to_model(item, workspace)
    elif isinstance(item, SourcedNodeV1):
        return source_node_v1_to_model(item, workspace)
    elif isinstance(item, SourcedEdgeSpec):
        return source_edge_v1_spec_to_model(item, workspace)
    elif isinstance(item, SourcedNodeSpec):
        return source_node_v1_spec_to_model(item, workspace)
    else:
        raise NotImplementedError(f"Cannot convert {type(item)} to a db model")


@multimethod
def model_to_schema(item, schema_type):
    raise NotImplementedError(f"Cannot convert {type(item)} to a {schema_type}")


@model_to_schema.register
def source_model_to_source_schema(model: Source, schema_type: Literal["SourceV1"]) -> SourceV1:
    return SourceV1.from_spec(model.__dict__)


@model_to_schema.register
def node_model_to_node_v1_schema(model: Node, schema_type: Literal["NodeV1"]) -> NodeV1:
    # TODO: Add data_sources

    data_sources: list[SourceV1] = model_to_schema(model.data_sources.all(), "SourceV1")
    result = NodeV1.from_spec({**model.__dict__, "data_sources": [source.spec for source in data_sources]})
    return result


@model_to_schema.register
def node_model_to_sourced_node_v1_schema(
    model: Node, source: Source, schema_type: Literal["SourcedNodeV1"]
) -> SourcedNodeV1:
    schema_source = model_to_schema(source, "SourceV1")
    return SourcedNodeV1.from_spec({**model.__dict__, "data_source": schema_source.spec})


@model_to_schema.register
def edge_model_to_edge_v1_schema(model: Edge, schema_type: Literal["EdgeV1"]) -> EdgeV1:
    # TODO: Add data_sources
    model_dict = {**model.__dict__, "data_sources": []}
    model_dict["source"] = NodeNamedID(**model.source.__dict__)
    model_dict["destination"] = NodeNamedID(**model.destination.__dict__)
    model_dict["destination"] = {"id": model_dict.pop("destination_id")}
    return EdgeV1.from_spec(model_dict)


@model_to_schema.register
def sequence_model_to_sequence_v1_schema(models: list[T] | tuple[T], schema_type: str) -> list[R]:
    result = list(model_to_schema(model, schema_type) for model in models)
    return result


@model_to_schema.register
def queryset_to_sequence_v1_schema(models: QuerySet[T], schema_type: str) -> list[R]:
    return [model_to_schema(model, schema_type) for model in models]
