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

export interface GetWorkspaceHome_workspace_tables_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetWorkspaceHome_workspace_tables {
  __typename: "TablePagination";
  meta: GetWorkspaceHome_workspace_tables_meta;
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
  source_graph: any;
  runs: GetWorkspaceHome_workspace_runs;
  tables: GetWorkspaceHome_workspace_tables;
  connections: GetWorkspaceHome_workspace_connections;
}

export interface GetWorkspaceHome {
  workspace: GetWorkspaceHome_workspace;
}

export interface GetWorkspaceHomeVariables {
  organisationName: string;
  workspaceName: string;
}
