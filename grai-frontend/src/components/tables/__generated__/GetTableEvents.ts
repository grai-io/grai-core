/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTableEvents
// ====================================================

export interface GetTableEvents_workspace_table_events_data_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
}

export interface GetTableEvents_workspace_table_events_data_connection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: GetTableEvents_workspace_table_events_data_connection_connector;
}

export interface GetTableEvents_workspace_table_events_data {
  __typename: "Event";
  id: any;
  date: any;
  status: string;
  connection: GetTableEvents_workspace_table_events_data_connection;
}

export interface GetTableEvents_workspace_table_events_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetTableEvents_workspace_table_events {
  __typename: "EventPagination";
  data: GetTableEvents_workspace_table_events_data[];
  meta: GetTableEvents_workspace_table_events_meta;
}

export interface GetTableEvents_workspace_table {
  __typename: "Table";
  id: any;
  events: GetTableEvents_workspace_table_events;
}

export interface GetTableEvents_workspace {
  __typename: "Workspace";
  id: any;
  table: GetTableEvents_workspace_table;
}

export interface GetTableEvents {
  workspace: GetTableEvents_workspace;
}

export interface GetTableEventsVariables {
  organisationName: string;
  workspaceName: string;
  tableId: string;
}
