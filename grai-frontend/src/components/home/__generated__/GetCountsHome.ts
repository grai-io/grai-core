/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetCountsHome
// ====================================================

export interface GetCountsHome_workspace_runs_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetCountsHome_workspace_runs {
  __typename: "RunPagination";
  meta: GetCountsHome_workspace_runs_meta;
}

export interface GetCountsHome_workspace_nodes_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetCountsHome_workspace_nodes {
  __typename: "NodePagination";
  meta: GetCountsHome_workspace_nodes_meta;
}

export interface GetCountsHome_workspace_connections_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetCountsHome_workspace_connections {
  __typename: "ConnectionPagination";
  meta: GetCountsHome_workspace_connections_meta;
}

export interface GetCountsHome_workspace {
  __typename: "Workspace";
  id: any;
  runs: GetCountsHome_workspace_runs;
  nodes: GetCountsHome_workspace_nodes;
  connections: GetCountsHome_workspace_connections;
}

export interface GetCountsHome {
  workspace: GetCountsHome_workspace;
}

export interface GetCountsHomeVariables {
  organisationName: string;
  workspaceName: string;
}
