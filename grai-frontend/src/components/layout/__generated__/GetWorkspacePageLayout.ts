/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspacePageLayout
// ====================================================

export interface GetWorkspacePageLayout_workspace_runs_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetWorkspacePageLayout_workspace_runs {
  __typename: "RunPagination";
  meta: GetWorkspacePageLayout_workspace_runs_meta;
}

export interface GetWorkspacePageLayout_workspace_nodes_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetWorkspacePageLayout_workspace_nodes {
  __typename: "NodePagination";
  meta: GetWorkspacePageLayout_workspace_nodes_meta;
}

export interface GetWorkspacePageLayout_workspace_connections_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetWorkspacePageLayout_workspace_connections {
  __typename: "ConnectionPagination";
  meta: GetWorkspacePageLayout_workspace_connections_meta;
}

export interface GetWorkspacePageLayout_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  runs: GetWorkspacePageLayout_workspace_runs;
  nodes: GetWorkspacePageLayout_workspace_nodes;
  connections: GetWorkspacePageLayout_workspace_connections;
}

export interface GetWorkspacePageLayout {
  workspace: GetWorkspacePageLayout_workspace;
}

export interface GetWorkspacePageLayoutVariables {
  organisationName: string;
  workspaceName: string;
}
