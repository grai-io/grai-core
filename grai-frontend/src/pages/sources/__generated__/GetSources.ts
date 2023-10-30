/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSources
// ====================================================

export interface GetSources_workspace_organisation {
  __typename: "Organisation";
  id: any;
}

export interface GetSources_workspace_sources_data_nodes_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetSources_workspace_sources_data_nodes {
  __typename: "NodePagination";
  meta: GetSources_workspace_sources_data_nodes_meta;
}

export interface GetSources_workspace_sources_data_edges_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetSources_workspace_sources_data_edges {
  __typename: "EdgePagination";
  meta: GetSources_workspace_sources_data_edges_meta;
}

export interface GetSources_workspace_sources_data_connections_data_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
}

export interface GetSources_workspace_sources_data_connections_data_last_run {
  __typename: "Run";
  id: any;
  status: string;
}

export interface GetSources_workspace_sources_data_connections_data {
  __typename: "Connection";
  id: any;
  name: string;
  connector: GetSources_workspace_sources_data_connections_data_connector;
  last_run: GetSources_workspace_sources_data_connections_data_last_run | null;
}

export interface GetSources_workspace_sources_data_connections {
  __typename: "ConnectionPagination";
  data: GetSources_workspace_sources_data_connections_data[];
}

export interface GetSources_workspace_sources_data {
  __typename: "Source";
  id: any;
  name: string;
  priority: number;
  nodes: GetSources_workspace_sources_data_nodes;
  edges: GetSources_workspace_sources_data_edges;
  connections: GetSources_workspace_sources_data_connections;
}

export interface GetSources_workspace_sources_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetSources_workspace_sources {
  __typename: "SourcePagination";
  data: GetSources_workspace_sources_data[];
  meta: GetSources_workspace_sources_meta;
}

export interface GetSources_workspace {
  __typename: "Workspace";
  id: any;
  sample_data: boolean;
  organisation: GetSources_workspace_organisation;
  sources: GetSources_workspace_sources;
}

export interface GetSources {
  workspace: GetSources_workspace;
}

export interface GetSourcesVariables {
  organisationName: string;
  workspaceName: string;
}
