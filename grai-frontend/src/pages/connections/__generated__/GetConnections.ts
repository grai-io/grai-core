/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnections
// ====================================================

export interface GetConnections_workspace_connections_data_connector {
  __typename: "Connector";
  id: any;
  name: string;
  events: boolean;
}

export interface GetConnections_workspace_connections_data_runs_data_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetConnections_workspace_connections_data_runs_data {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetConnections_workspace_connections_data_runs_data_user | null;
  metadata: any;
}

export interface GetConnections_workspace_connections_data_runs_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetConnections_workspace_connections_data_runs {
  __typename: "RunPagination";
  data: GetConnections_workspace_connections_data_runs_data[];
  meta: GetConnections_workspace_connections_data_runs_meta;
}

export interface GetConnections_workspace_connections_data_last_run_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetConnections_workspace_connections_data_last_run {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetConnections_workspace_connections_data_last_run_user | null;
  metadata: any;
}

export interface GetConnections_workspace_connections_data_last_successful_run_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetConnections_workspace_connections_data_last_successful_run {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: GetConnections_workspace_connections_data_last_successful_run_user | null;
  metadata: any;
}

export interface GetConnections_workspace_connections_data {
  __typename: "Connection";
  id: any;
  namespace: string;
  name: string;
  is_active: boolean;
  validated: boolean;
  connector: GetConnections_workspace_connections_data_connector;
  runs: GetConnections_workspace_connections_data_runs;
  last_run: GetConnections_workspace_connections_data_last_run | null;
  last_successful_run: GetConnections_workspace_connections_data_last_successful_run | null;
}

export interface GetConnections_workspace_connections_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetConnections_workspace_connections {
  __typename: "ConnectionPagination";
  data: GetConnections_workspace_connections_data[];
  meta: GetConnections_workspace_connections_meta;
}

export interface GetConnections_workspace {
  __typename: "Workspace";
  id: any;
  connections: GetConnections_workspace_connections;
}

export interface GetConnections {
  workspace: GetConnections_workspace;
}

export interface GetConnectionsVariables {
  organisationName: string;
  workspaceName: string;
}
