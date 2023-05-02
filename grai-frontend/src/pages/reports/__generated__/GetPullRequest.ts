/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetPullRequest
// ====================================================

export interface GetPullRequest_workspace_repository_pull_request_last_commit_last_successful_run {
  __typename: "Run";
  id: any;
  metadata: any;
  created_at: any;
}

export interface GetPullRequest_workspace_repository_pull_request_last_commit {
  __typename: "Commit";
  id: any;
  reference: string;
  created_at: any;
  last_successful_run: GetPullRequest_workspace_repository_pull_request_last_commit_last_successful_run | null;
}

export interface GetPullRequest_workspace_repository_pull_request_branch {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetPullRequest_workspace_repository_pull_request {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
  last_commit: GetPullRequest_workspace_repository_pull_request_last_commit | null;
  branch: GetPullRequest_workspace_repository_pull_request_branch;
}

export interface GetPullRequest_workspace_repository {
  __typename: "Repository";
  id: any;
  owner: string;
  repo: string;
  pull_request: GetPullRequest_workspace_repository_pull_request;
}

export interface GetPullRequest_workspace_tables_data_columns_data {
  __typename: "Column";
  id: any;
  name: string;
}

export interface GetPullRequest_workspace_tables_data_columns {
  __typename: "ColumnDataWrapper";
  data: GetPullRequest_workspace_tables_data_columns_data[];
}

export interface GetPullRequest_workspace_tables_data_source_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetPullRequest_workspace_tables_data_source_tables {
  __typename: "TableDataWrapper";
  data: GetPullRequest_workspace_tables_data_source_tables_data[];
}

export interface GetPullRequest_workspace_tables_data_destination_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetPullRequest_workspace_tables_data_destination_tables {
  __typename: "TableDataWrapper";
  data: GetPullRequest_workspace_tables_data_destination_tables_data[];
}

export interface GetPullRequest_workspace_tables_data {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  metadata: any;
  columns: GetPullRequest_workspace_tables_data_columns;
  source_tables: GetPullRequest_workspace_tables_data_source_tables;
  destination_tables: GetPullRequest_workspace_tables_data_destination_tables;
}

export interface GetPullRequest_workspace_tables {
  __typename: "TablePagination";
  data: GetPullRequest_workspace_tables_data[];
}

export interface GetPullRequest_workspace_other_edges_data_source {
  __typename: "Node";
  id: any;
}

export interface GetPullRequest_workspace_other_edges_data_destination {
  __typename: "Node";
  id: any;
}

export interface GetPullRequest_workspace_other_edges_data {
  __typename: "Edge";
  id: any;
  source: GetPullRequest_workspace_other_edges_data_source;
  destination: GetPullRequest_workspace_other_edges_data_destination;
  metadata: any;
}

export interface GetPullRequest_workspace_other_edges {
  __typename: "EdgePagination";
  data: GetPullRequest_workspace_other_edges_data[];
}

export interface GetPullRequest_workspace_filters_data {
  __typename: "Filter";
  id: any;
  name: string | null;
}

export interface GetPullRequest_workspace_filters {
  __typename: "FilterPagination";
  data: GetPullRequest_workspace_filters_data[];
}

export interface GetPullRequest_workspace {
  __typename: "Workspace";
  id: any;
  repository: GetPullRequest_workspace_repository;
  tables: GetPullRequest_workspace_tables;
  other_edges: GetPullRequest_workspace_other_edges;
  filters: GetPullRequest_workspace_filters;
}

export interface GetPullRequest {
  workspace: GetPullRequest_workspace;
}

export interface GetPullRequestVariables {
  organisationName: string;
  workspaceName: string;
  type: string;
  owner: string;
  repo: string;
  reference: string;
}
