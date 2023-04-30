/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetReportsHome
// ====================================================

export interface GetReportsHome_workspace_runs_data_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
}

export interface GetReportsHome_workspace_runs_data_connection {
  __typename: "Connection";
  id: any;
  name: string;
  temp: boolean;
  connector: GetReportsHome_workspace_runs_data_connection_connector;
}

export interface GetReportsHome_workspace_runs_data_commit_branch {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetReportsHome_workspace_runs_data_commit_pull_request {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
}

export interface GetReportsHome_workspace_runs_data_commit_repository {
  __typename: "Repository";
  id: any;
  type: string;
  owner: string;
  repo: string;
}

export interface GetReportsHome_workspace_runs_data_commit {
  __typename: "Commit";
  id: any;
  reference: string;
  title: string | null;
  branch: GetReportsHome_workspace_runs_data_commit_branch;
  pull_request: GetReportsHome_workspace_runs_data_commit_pull_request | null;
  repository: GetReportsHome_workspace_runs_data_commit_repository;
}

export interface GetReportsHome_workspace_runs_data_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetReportsHome_workspace_runs_data {
  __typename: "Run";
  id: any;
  status: string;
  connection: GetReportsHome_workspace_runs_data_connection;
  commit: GetReportsHome_workspace_runs_data_commit | null;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetReportsHome_workspace_runs_data_user | null;
  metadata: any;
}

export interface GetReportsHome_workspace_runs {
  __typename: "RunPagination";
  data: GetReportsHome_workspace_runs_data[];
}

export interface GetReportsHome_workspace {
  __typename: "Workspace";
  id: any;
  runs: GetReportsHome_workspace_runs;
}

export interface GetReportsHome {
  workspace: GetReportsHome_workspace;
}

export interface GetReportsHomeVariables {
  organisationName: string;
  workspaceName: string;
}
