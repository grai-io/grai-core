/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: RunConnection
// ====================================================

export interface RunConnection_runConnection_connection_last_run_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface RunConnection_runConnection_connection_last_run {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  metadata: any;
  user: RunConnection_runConnection_connection_last_run_user | null;
}

export interface RunConnection_runConnection_connection_last_successful_run_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface RunConnection_runConnection_connection_last_successful_run {
  __typename: "Run";
  id: any;
  status: string;
  started_at: any | null;
  finished_at: any | null;
  metadata: any;
  user: RunConnection_runConnection_connection_last_successful_run_user | null;
}

export interface RunConnection_runConnection_connection_runs_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface RunConnection_runConnection_connection_runs {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: RunConnection_runConnection_connection_runs_user | null;
  metadata: any;
}

export interface RunConnection_runConnection_connection {
  __typename: "Connection";
  id: any;
  last_run: RunConnection_runConnection_connection_last_run | null;
  last_successful_run: RunConnection_runConnection_connection_last_successful_run | null;
  runs: RunConnection_runConnection_connection_runs[];
}

export interface RunConnection_runConnection {
  __typename: "Run";
  id: any;
  connection: RunConnection_runConnection_connection;
}

export interface RunConnection {
  runConnection: RunConnection_runConnection;
}

export interface RunConnectionVariables {
  connectionId: string;
}
