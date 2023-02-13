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

export interface GetPullRequest_workspace_tables_columns {
  __typename: "Column";
  id: any;
  name: string;
}

export interface GetPullRequest_workspace_tables_source_tables {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetPullRequest_workspace_tables_destination_tables {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetPullRequest_workspace_tables {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  metadata: any;
  columns: GetPullRequest_workspace_tables_columns[];
  source_tables: GetPullRequest_workspace_tables_source_tables[];
  destination_tables: GetPullRequest_workspace_tables_destination_tables[];
}

export interface GetPullRequest_workspace_other_edges_source {
  __typename: "Node";
  id: any;
}

export interface GetPullRequest_workspace_other_edges_destination {
  __typename: "Node";
  id: any;
}

export interface GetPullRequest_workspace_other_edges {
  __typename: "Edge";
  id: any;
  source: GetPullRequest_workspace_other_edges_source;
  destination: GetPullRequest_workspace_other_edges_destination;
  metadata: any;
}

export interface GetPullRequest_workspace {
  __typename: "Workspace";
  id: any;
  repository: GetPullRequest_workspace_repository;
  tables: GetPullRequest_workspace_tables[];
  other_edges: GetPullRequest_workspace_other_edges[];
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
