from grai_schemas.v1.source import SourceV1, SourceSpec
from grai_schemas.v1.node import NodeSpec, SourcedNodeSpec, NodeV1, SourcedNodeV1
from grai_schemas.v1.edge import EdgeSpec, SourcedEdgeSpec, EdgeV1, SourcedEdgeV1
from grai_schemas.v1.workspace import WorkspaceSpec, WorkspaceV1
from grai_schemas.v1.organization import OrganisationSpec, OrganisationV1
from lineage.models import Edge, Node, Source
from workspaces.models import Workspace, Organisation
from typing import Optional, Any, Sequence, List
from uuid import UUID
import pprint
from django.db.models import Q


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


def workspace_v1_spec_to_model(workspace_arg: WorkspaceSpec, workspace: Optional[Workspace] = None) -> Workspace:
    raise NotImplementedError()


def workspace_v1_to_model(workspace_arg: WorkspaceV1, workspace: Optional[Workspace] = None) -> Workspace:
    return workspace_v1_spec_to_model(workspace_arg.spec, workspace)


def source_v1_spec_to_model(source: SourceSpec, workspace: Optional[Workspace] = None) -> Source:
    obj_workspace = source.workspace if workspace is None else workspace
    if obj_workspace is None:
        raise ValueError("Workspace must be provided either on the source or as an argument to this function")

    return Source(name=source.name, workspace=obj_workspace)


def source_v1_to_model(source: SourceV1, workspace: Optional[Workspace] = None) -> Source:
    return source_v1_spec_to_model(source.spec, workspace)


def source_node_v1_spec_to_model(source_node: SourcedNodeSpec, workspace: Optional[Workspace] = None) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return node_v1_spec_to_model(source_node.to_node(), workspace)


def source_node_v1_to_model(source_node: SourcedNodeV1, workspace: Optional[Workspace] = None) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return source_node_v1_spec_to_model(source_node.spec, workspace)


def node_v1_spec_to_model(node: NodeSpec, workspace: Optional[Workspace] = None) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    obj_workspace = node.workspace if workspace is None else workspace
    if obj_workspace is None:
        raise ValueError("Workspace must be provided either on the source or as an argument to this function")

    values = node.dict(exclude={"data_sources", "workspace"}) | {"workspace": workspace}

    result = Node(**values)
    result.set_names()

    return result


def node_v1_to_model(node: NodeV1, workspace: Optional[Workspace] = None) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return node_v1_spec_to_model(node.spec, workspace)


def source_edge_v1_spec_to_model(source_edge: SourcedEdgeSpec, workspace: Optional[Workspace] = None) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return edge_v1_spec_to_model(source_edge.to_edge(), workspace)


def source_edge_v1_to_model(source_edge: SourcedEdgeV1, workspace: Optional[Workspace] = None) -> Node:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    return source_edge_v1_spec_to_model(source_edge.spec, workspace)


def edge_v1_spec_to_model(edge: EdgeSpec, workspace: Optional[Workspace] = None) -> Edge:
    """
    WARNING: Does not set ManyToMany relationships like data_sources for performance reasons.
    """
    obj_workspace = edge.workspace if workspace is None else workspace
    if obj_workspace is None:
        raise ValueError("Workspace must be provided either on the source or as an argument to this function")

    values = edge.dict(exclude={"workspace", "data_sources"}) | {"workspace": workspace}

    if edge.source.id is None or edge.destination.id is None:
        source_name = Q(name=edge.source.name, namespace=edge.source.namespace)
        destination_name = Q(name=edge.destination.name, namespace=edge.destination.namespace)
        workspace_filter = Q(workspace=obj_workspace)
        query = (source_name | destination_name) & workspace_filter

        nodes = Node.objects.filter(query).all()
        if len(nodes) != 2:
            raise ValueError(
                f"Could not find the source and destination nodes for edge name={edge.name}, namespace={edge.namespace}"
                f" in the `{workspace}` workspace."
            )
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


def edge_v1_to_model(edge: EdgeV1, workspace: Optional[Workspace] = None) -> Edge:
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
