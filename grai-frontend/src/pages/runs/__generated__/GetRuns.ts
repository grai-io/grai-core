/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRuns
// ====================================================

export interface GetRuns_workspace_runs_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
}

export interface GetRuns_workspace_runs_connection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: GetRuns_workspace_runs_connection_connector;
}

export interface GetRuns_workspace_runs_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetRuns_workspace_runs {
  __typename: "Run";
  id: any;
  status: string;
  connection: GetRuns_workspace_runs_connection;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetRuns_workspace_runs_user | null;
  metadata: any;
}

export interface GetRuns_workspace {
  __typename: "Workspace";
  id: any;
  runs: GetRuns_workspace_runs[];
}

export interface GetRuns {
  workspace: GetRuns_workspace;
}

export interface GetRunsVariables {
  organisationName: string;
  workspaceName: string;
}
