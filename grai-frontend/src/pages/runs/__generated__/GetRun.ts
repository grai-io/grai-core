/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRun
// ====================================================

export interface GetRun_workspace_run_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
}

export interface GetRun_workspace_run_connection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: GetRun_workspace_run_connection_connector;
}

export interface GetRun_workspace_run_user {
  __typename: "User";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface GetRun_workspace_run {
  __typename: "Run";
  id: any;
  connection: GetRun_workspace_run_connection;
  status: string;
  metadata: any;
  created_at: any;
  updated_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetRun_workspace_run_user | null;
}

export interface GetRun_workspace {
  __typename: "Workspace";
  id: any;
  run: GetRun_workspace_run;
}

export interface GetRun {
  workspace: GetRun_workspace;
}

export interface GetRunVariables {
  organisationName: string;
  workspaceName: string;
  runId: string;
}
