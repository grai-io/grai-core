/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceHome
// ====================================================

export interface GetWorkspaceHome_workspace_runs_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetWorkspaceHome_workspace_runs {
  __typename: "RunPagination";
  meta: GetWorkspaceHome_workspace_runs_meta;
}

export interface GetWorkspaceHome_workspace_nodes_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetWorkspaceHome_workspace_nodes {
  __typename: "NodePagination";
  meta: GetWorkspaceHome_workspace_nodes_meta;
}

export interface GetWorkspaceHome_workspace_connections_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetWorkspaceHome_workspace_connections {
  __typename: "ConnectionPagination";
  meta: GetWorkspaceHome_workspace_connections_meta;
}

export interface GetWorkspaceHome_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  runs: GetWorkspaceHome_workspace_runs;
  nodes: GetWorkspaceHome_workspace_nodes;
  connections: GetWorkspaceHome_workspace_connections;
}

export interface GetWorkspaceHome {
  workspace: GetWorkspaceHome_workspace;
}

export interface GetWorkspaceHomeVariables {
  organisationName: string;
  workspaceName: string;
}
