/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceRuns
// ====================================================

export interface GetWorkspaceRuns_workspace_runs_data_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
}

export interface GetWorkspaceRuns_workspace_runs_data_connection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: GetWorkspaceRuns_workspace_runs_data_connection_connector;
}

export interface GetWorkspaceRuns_workspace_runs_data_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetWorkspaceRuns_workspace_runs_data {
  __typename: "Run";
  id: any;
  status: string;
  connection: GetWorkspaceRuns_workspace_runs_data_connection;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetWorkspaceRuns_workspace_runs_data_user | null;
  metadata: any;
}

export interface GetWorkspaceRuns_workspace_runs {
  __typename: "RunPagination";
  data: GetWorkspaceRuns_workspace_runs_data[];
}

export interface GetWorkspaceRuns_workspace {
  __typename: "Workspace";
  id: any;
  runs: GetWorkspaceRuns_workspace_runs;
}

export interface GetWorkspaceRuns {
  workspace: GetWorkspaceRuns_workspace;
}

export interface GetWorkspaceRunsVariables {
  workspaceId: string;
}
