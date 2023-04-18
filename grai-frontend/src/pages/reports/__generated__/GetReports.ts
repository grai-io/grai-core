/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetReports
// ====================================================

export interface GetReports_workspace_repositories_data_branches_data {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetReports_workspace_repositories_data_branches {
  __typename: "BranchPagination";
  data: GetReports_workspace_repositories_data_branches_data[];
}

export interface GetReports_workspace_repositories_data_pull_requests_data {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
}

export interface GetReports_workspace_repositories_data_pull_requests {
  __typename: "PullRequestPagination";
  data: GetReports_workspace_repositories_data_pull_requests_data[];
}

export interface GetReports_workspace_repositories_data {
  __typename: "Repository";
  id: any;
  type: string;
  owner: string;
  repo: string;
  branches: GetReports_workspace_repositories_data_branches;
  pull_requests: GetReports_workspace_repositories_data_pull_requests;
}

export interface GetReports_workspace_repositories {
  __typename: "RepositoryPagination";
  data: GetReports_workspace_repositories_data[];
}

export interface GetReports_workspace_runs_data_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
}

export interface GetReports_workspace_runs_data_connection {
  __typename: "Connection";
  id: any;
  name: string;
  temp: boolean;
  connector: GetReports_workspace_runs_data_connection_connector;
}

export interface GetReports_workspace_runs_data_commit_branch {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetReports_workspace_runs_data_commit_pull_request {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
}

export interface GetReports_workspace_runs_data_commit_repository {
  __typename: "Repository";
  id: any;
  type: string;
  owner: string;
  repo: string;
}

export interface GetReports_workspace_runs_data_commit {
  __typename: "Commit";
  id: any;
  reference: string;
  title: string | null;
  branch: GetReports_workspace_runs_data_commit_branch;
  pull_request: GetReports_workspace_runs_data_commit_pull_request | null;
  repository: GetReports_workspace_runs_data_commit_repository;
}

export interface GetReports_workspace_runs_data_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetReports_workspace_runs_data {
  __typename: "Run";
  id: any;
  status: string;
  connection: GetReports_workspace_runs_data_connection;
  commit: GetReports_workspace_runs_data_commit | null;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetReports_workspace_runs_data_user | null;
  metadata: any;
}

export interface GetReports_workspace_runs {
  __typename: "RunPagination";
  data: GetReports_workspace_runs_data[];
}

export interface GetReports_workspace {
  __typename: "Workspace";
  id: any;
  repositories: GetReports_workspace_repositories;
  runs: GetReports_workspace_runs;
}

export interface GetReports {
  workspace: GetReports_workspace;
}

export interface GetReportsVariables {
  organisationName: string;
  workspaceName: string;
  owner?: string | null;
  repo?: string | null;
  branch?: string | null;
}
