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

export interface GetCountsHome_workspace_sources_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetCountsHome_workspace_sources {
  __typename: "SourcePagination";
  meta: GetCountsHome_workspace_sources_meta;
}

export interface GetCountsHome_workspace {
  __typename: "Workspace";
  id: any;
  runs: GetCountsHome_workspace_runs;
  nodes: GetCountsHome_workspace_nodes;
  sources: GetCountsHome_workspace_sources;
}

export interface GetCountsHome {
  workspace: GetCountsHome_workspace;
}

export interface GetCountsHomeVariables {
  organisationName: string;
  workspaceName: string;
}
