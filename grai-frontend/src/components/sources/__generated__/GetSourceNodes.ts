/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSourceNodes
// ====================================================

export interface GetSourceNodes_workspace_source_nodes_data_data_sources_data_connections_data_connector {
  __typename: "Connector";
  id: any;
  name: string;
  slug: string | null;
}

export interface GetSourceNodes_workspace_source_nodes_data_data_sources_data_connections_data {
  __typename: "Connection";
  id: any;
  connector: GetSourceNodes_workspace_source_nodes_data_data_sources_data_connections_data_connector;
}

export interface GetSourceNodes_workspace_source_nodes_data_data_sources_data_connections {
  __typename: "ConnectionPagination";
  data: GetSourceNodes_workspace_source_nodes_data_data_sources_data_connections_data[];
}

export interface GetSourceNodes_workspace_source_nodes_data_data_sources_data {
  __typename: "Source";
  id: any;
  name: string;
  connections: GetSourceNodes_workspace_source_nodes_data_data_sources_data_connections;
}

export interface GetSourceNodes_workspace_source_nodes_data_data_sources {
  __typename: "SourcePagination";
  data: GetSourceNodes_workspace_source_nodes_data_data_sources_data[];
}

export interface GetSourceNodes_workspace_source_nodes_data {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  metadata: any;
  data_sources: GetSourceNodes_workspace_source_nodes_data_data_sources;
}

export interface GetSourceNodes_workspace_source_nodes_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetSourceNodes_workspace_source_nodes {
  __typename: "NodePagination";
  data: GetSourceNodes_workspace_source_nodes_data[];
  meta: GetSourceNodes_workspace_source_nodes_meta;
}

export interface GetSourceNodes_workspace_source {
  __typename: "Source";
  id: any;
  nodes: GetSourceNodes_workspace_source_nodes;
}

export interface GetSourceNodes_workspace {
  __typename: "Workspace";
  id: any;
  source: GetSourceNodes_workspace_source;
}

export interface GetSourceNodes {
  workspace: GetSourceNodes_workspace;
}

export interface GetSourceNodesVariables {
  workspaceId: string;
  sourceId: string;
  offset?: number | null;
  search?: string | null;
}
