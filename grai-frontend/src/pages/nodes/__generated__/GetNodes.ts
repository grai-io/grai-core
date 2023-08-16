/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { WorkspaceNodeFilter, NodeOrder } from "./../../../../__generated__/globalTypes";

// ====================================================
// GraphQL query operation: GetNodes
// ====================================================

export interface GetNodes_workspace_nodes_data_data_sources_data_connections_data_connector {
  __typename: "Connector";
  id: any;
  name: string;
  slug: string | null;
}

export interface GetNodes_workspace_nodes_data_data_sources_data_connections_data {
  __typename: "Connection";
  id: any;
  connector: GetNodes_workspace_nodes_data_data_sources_data_connections_data_connector;
}

export interface GetNodes_workspace_nodes_data_data_sources_data_connections {
  __typename: "ConnectionPagination";
  data: GetNodes_workspace_nodes_data_data_sources_data_connections_data[];
}

export interface GetNodes_workspace_nodes_data_data_sources_data {
  __typename: "Source";
  id: any;
  name: string;
  connections: GetNodes_workspace_nodes_data_data_sources_data_connections;
}

export interface GetNodes_workspace_nodes_data_data_sources {
  __typename: "SourcePagination";
  data: GetNodes_workspace_nodes_data_data_sources_data[];
}

export interface GetNodes_workspace_nodes_data {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  metadata: any;
  data_sources: GetNodes_workspace_nodes_data_data_sources;
}

export interface GetNodes_workspace_nodes_meta {
  __typename: "PaginationResult";
  filtered: number;
  total: number;
}

export interface GetNodes_workspace_nodes {
  __typename: "NodePagination";
  data: GetNodes_workspace_nodes_data[];
  meta: GetNodes_workspace_nodes_meta;
}

export interface GetNodes_workspace {
  __typename: "Workspace";
  id: any;
  nodes: GetNodes_workspace_nodes;
}

export interface GetNodes {
  workspace: GetNodes_workspace;
}

export interface GetNodesVariables {
  organisationName: string;
  workspaceName: string;
  offset?: number | null;
  search?: string | null;
  filter?: WorkspaceNodeFilter | null;
  order?: NodeOrder | null;
}
