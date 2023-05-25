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

export interface GetPullRequest_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  destinations: string[];
}

export interface GetPullRequest_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  namespace: string;
  data_source: string;
  columns: GetPullRequest_workspace_graph_columns[];
  destinations: string[];
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
  graph: GetPullRequest_workspace_graph[];
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
