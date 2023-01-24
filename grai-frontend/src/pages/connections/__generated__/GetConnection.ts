/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnection
// ====================================================

export interface GetConnection_workspace_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  metadata: any;
}

export interface GetConnection_workspace_connection_last_run_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetConnection_workspace_connection_last_run {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  metadata: any;
  user: GetConnection_workspace_connection_last_run_user | null;
}

export interface GetConnection_workspace_connection_last_successful_run_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetConnection_workspace_connection_last_successful_run {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  metadata: any;
  user: GetConnection_workspace_connection_last_successful_run_user | null;
}

export interface GetConnection_workspace_connection_runs_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetConnection_workspace_connection_runs {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetConnection_workspace_connection_runs_user | null;
  metadata: any;
}

export interface GetConnection_workspace_connection {
  __typename: "Connection";
  id: any;
  namespace: string;
  name: string;
  connector: GetConnection_workspace_connection_connector;
  metadata: any;
  schedules: any | null;
  is_active: boolean;
  created_at: any;
  updated_at: any;
  last_run: GetConnection_workspace_connection_last_run | null;
  last_successful_run: GetConnection_workspace_connection_last_successful_run | null;
  runs: GetConnection_workspace_connection_runs[];
}

export interface GetConnection_workspace {
  __typename: "Workspace";
  id: any;
  connection: GetConnection_workspace_connection;
}

export interface GetConnection {
  workspace: GetConnection_workspace;
}

export interface GetConnectionVariables {
  organisationName: string;
  workspaceName: string;
  connectionId: string;
}
