/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { WorkspaceEdgeFilter } from "./../../../../__generated__/globalTypes";

// ====================================================
// GraphQL query operation: GetEdges
// ====================================================

export interface GetEdges_workspace_edges_data_source {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
}

export interface GetEdges_workspace_edges_data_destination {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
}

export interface GetEdges_workspace_edges_data_data_sources_data_connections_data_connector {
  __typename: "Connector";
  id: any;
  name: string;
  slug: string | null;
}

export interface GetEdges_workspace_edges_data_data_sources_data_connections_data {
  __typename: "Connection";
  id: any;
  connector: GetEdges_workspace_edges_data_data_sources_data_connections_data_connector;
}

export interface GetEdges_workspace_edges_data_data_sources_data_connections {
  __typename: "ConnectionPagination";
  data: GetEdges_workspace_edges_data_data_sources_data_connections_data[];
}

export interface GetEdges_workspace_edges_data_data_sources_data {
  __typename: "Source";
  id: any;
  name: string;
  connections: GetEdges_workspace_edges_data_data_sources_data_connections;
}

export interface GetEdges_workspace_edges_data_data_sources {
  __typename: "SourcePagination";
  data: GetEdges_workspace_edges_data_data_sources_data[];
}

export interface GetEdges_workspace_edges_data {
  __typename: "Edge";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  metadata: any;
  source: GetEdges_workspace_edges_data_source;
  destination: GetEdges_workspace_edges_data_destination;
  data_sources: GetEdges_workspace_edges_data_data_sources;
}

export interface GetEdges_workspace_edges_meta {
  __typename: "PaginationResult";
  filtered: number;
  total: number;
}

export interface GetEdges_workspace_edges {
  __typename: "EdgePagination";
  data: GetEdges_workspace_edges_data[];
  meta: GetEdges_workspace_edges_meta;
}

export interface GetEdges_workspace {
  __typename: "Workspace";
  id: any;
  edges: GetEdges_workspace_edges;
}

export interface GetEdges {
  workspace: GetEdges_workspace;
}

export interface GetEdgesVariables {
  organisationName: string;
  workspaceName: string;
  offset?: number | null;
  search?: string | null;
  filter?: WorkspaceEdgeFilter | null;
}
