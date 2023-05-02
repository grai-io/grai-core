/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetCommit
// ====================================================

export interface GetCommit_workspace_repository_commit_last_successful_run {
  __typename: "Run";
  id: any;
  metadata: any;
  created_at: any;
}

export interface GetCommit_workspace_repository_commit_branch {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetCommit_workspace_repository_commit_pull_request {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
}

export interface GetCommit_workspace_repository_commit {
  __typename: "Commit";
  id: any;
  reference: string;
  title: string | null;
  created_at: any;
  last_successful_run: GetCommit_workspace_repository_commit_last_successful_run | null;
  branch: GetCommit_workspace_repository_commit_branch;
  pull_request: GetCommit_workspace_repository_commit_pull_request | null;
}

export interface GetCommit_workspace_repository {
  __typename: "Repository";
  id: any;
  owner: string;
  repo: string;
  commit: GetCommit_workspace_repository_commit;
}

export interface GetCommit_workspace_tables_data_columns_data {
  __typename: "Column";
  id: any;
  name: string;
}

export interface GetCommit_workspace_tables_data_columns {
  __typename: "ColumnDataWrapper";
  data: GetCommit_workspace_tables_data_columns_data[];
}

export interface GetCommit_workspace_tables_data_source_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetCommit_workspace_tables_data_source_tables {
  __typename: "TableDataWrapper";
  data: GetCommit_workspace_tables_data_source_tables_data[];
}

export interface GetCommit_workspace_tables_data_destination_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetCommit_workspace_tables_data_destination_tables {
  __typename: "TableDataWrapper";
  data: GetCommit_workspace_tables_data_destination_tables_data[];
}

export interface GetCommit_workspace_tables_data {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  metadata: any;
  columns: GetCommit_workspace_tables_data_columns;
  source_tables: GetCommit_workspace_tables_data_source_tables;
  destination_tables: GetCommit_workspace_tables_data_destination_tables;
}

export interface GetCommit_workspace_tables {
  __typename: "TablePagination";
  data: GetCommit_workspace_tables_data[];
}

export interface GetCommit_workspace_other_edges_data_source {
  __typename: "Node";
  id: any;
}

export interface GetCommit_workspace_other_edges_data_destination {
  __typename: "Node";
  id: any;
}

export interface GetCommit_workspace_other_edges_data {
  __typename: "Edge";
  id: any;
  source: GetCommit_workspace_other_edges_data_source;
  destination: GetCommit_workspace_other_edges_data_destination;
  metadata: any;
}

export interface GetCommit_workspace_other_edges {
  __typename: "EdgePagination";
  data: GetCommit_workspace_other_edges_data[];
}

export interface GetCommit_workspace {
  __typename: "Workspace";
  id: any;
  repository: GetCommit_workspace_repository;
  tables: GetCommit_workspace_tables;
  other_edges: GetCommit_workspace_other_edges;
}

export interface GetCommit {
  workspace: GetCommit_workspace;
}

export interface GetCommitVariables {
  organisationName: string;
  workspaceName: string;
  type: string;
  owner: string;
  repo: string;
  reference: string;
}
