/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnectionEvents
// ====================================================

export interface GetConnectionEvents_workspace_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  metadata: any;
  icon: string | null;
}

export interface GetConnectionEvents_workspace_connection_last_run_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetConnectionEvents_workspace_connection_last_run {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  metadata: any;
  user: GetConnectionEvents_workspace_connection_last_run_user | null;
}

export interface GetConnectionEvents_workspace_connection_last_successful_run_user {
  __typename: "User";
  id: any;
  first_name: string;
  last_name: string;
}

export interface GetConnectionEvents_workspace_connection_last_successful_run {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  metadata: any;
  user: GetConnectionEvents_workspace_connection_last_successful_run_user | null;
}

export interface GetConnectionEvents_workspace_connection_events_data {
  __typename: "Event";
  id: any;
  date: any;
  status: string;
  created_at: any;
}

export interface GetConnectionEvents_workspace_connection_events_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetConnectionEvents_workspace_connection_events {
  __typename: "EventPagination";
  data: GetConnectionEvents_workspace_connection_events_data[];
  meta: GetConnectionEvents_workspace_connection_events_meta;
}

export interface GetConnectionEvents_workspace_connection {
  __typename: "Connection";
  id: any;
  namespace: string;
  name: string;
  connector: GetConnectionEvents_workspace_connection_connector;
  metadata: any;
  schedules: any | null;
  is_active: boolean;
  created_at: any;
  updated_at: any;
  last_run: GetConnectionEvents_workspace_connection_last_run | null;
  last_successful_run: GetConnectionEvents_workspace_connection_last_successful_run | null;
  events: GetConnectionEvents_workspace_connection_events;
}

export interface GetConnectionEvents_workspace {
  __typename: "Workspace";
  id: any;
  connection: GetConnectionEvents_workspace_connection;
}

export interface GetConnectionEvents {
  workspace: GetConnectionEvents_workspace;
}

export interface GetConnectionEventsVariables {
  organisationName: string;
  workspaceName: string;
  connectionId: string;
}
