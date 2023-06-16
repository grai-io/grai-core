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

export interface GetCommit_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  display_name: string;
  destinations: string[];
}

export interface GetCommit_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  display_name: string;
  namespace: string;
  x: number;
  y: number;
  data_source: string;
  columns: GetCommit_workspace_graph_columns[];
  destinations: string[];
}

export interface GetCommit_workspace {
  __typename: "Workspace";
  id: any;
  repository: GetCommit_workspace_repository;
  graph: GetCommit_workspace_graph[];
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
