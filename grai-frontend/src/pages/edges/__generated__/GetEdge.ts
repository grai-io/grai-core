/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetEdge
// ====================================================

export interface GetEdge_workspace_edge_source {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
}

export interface GetEdge_workspace_edge_destination {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
}

export interface GetEdge_workspace_edge_data_sources_data_connections_data_connector {
  __typename: "Connector";
  id: any;
  name: string;
  slug: string | null;
}

export interface GetEdge_workspace_edge_data_sources_data_connections_data {
  __typename: "Connection";
  id: any;
  connector: GetEdge_workspace_edge_data_sources_data_connections_data_connector;
}

export interface GetEdge_workspace_edge_data_sources_data_connections {
  __typename: "ConnectionPagination";
  data: GetEdge_workspace_edge_data_sources_data_connections_data[];
}

export interface GetEdge_workspace_edge_data_sources_data {
  __typename: "Source";
  id: any;
  name: string;
  connections: GetEdge_workspace_edge_data_sources_data_connections;
}

export interface GetEdge_workspace_edge_data_sources {
  __typename: "SourcePagination";
  data: GetEdge_workspace_edge_data_sources_data[];
}

export interface GetEdge_workspace_edge {
  __typename: "Edge";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  metadata: any;
  source: GetEdge_workspace_edge_source;
  destination: GetEdge_workspace_edge_destination;
  data_sources: GetEdge_workspace_edge_data_sources;
}

export interface GetEdge_workspace {
  __typename: "Workspace";
  id: any;
  edge: GetEdge_workspace_edge;
}

export interface GetEdge {
  workspace: GetEdge_workspace;
}

export interface GetEdgeVariables {
  organisationName: string;
  workspaceName: string;
  edgeId: string;
}
