/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTable
// ====================================================

export interface GetTable_workspace_table_columns_data_requirements_edges_data_destination {
  __typename: "Node";
  id: any;
  name: string;
  display_name: string;
  metadata: any;
}

export interface GetTable_workspace_table_columns_data_requirements_edges_data {
  __typename: "Edge";
  id: any;
  metadata: any;
  destination: GetTable_workspace_table_columns_data_requirements_edges_data_destination;
}

export interface GetTable_workspace_table_columns_data_requirements_edges {
  __typename: "EdgePagination";
  data: GetTable_workspace_table_columns_data_requirements_edges_data[];
}

export interface GetTable_workspace_table_columns_data {
  __typename: "Column";
  id: any;
  name: string;
  display_name: string;
  requirements_edges: GetTable_workspace_table_columns_data_requirements_edges;
  metadata: any;
}

export interface GetTable_workspace_table_columns {
  __typename: "ColumnDataWrapper";
  data: GetTable_workspace_table_columns_data[];
}

export interface GetTable_workspace_table_source_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTable_workspace_table_source_tables {
  __typename: "TableDataWrapper";
  data: GetTable_workspace_table_source_tables_data[];
}

export interface GetTable_workspace_table_destination_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTable_workspace_table_destination_tables {
  __typename: "TableDataWrapper";
  data: GetTable_workspace_table_destination_tables_data[];
}

export interface GetTable_workspace_table_sources_data {
  __typename: "Source";
  id: any;
  name: string;
}

export interface GetTable_workspace_table_sources {
  __typename: "SourcePagination";
  data: GetTable_workspace_table_sources_data[];
}

export interface GetTable_workspace_table_events_data_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
}

export interface GetTable_workspace_table_events_data_connection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: GetTable_workspace_table_events_data_connection_connector;
}

export interface GetTable_workspace_table_events_data {
  __typename: "Event";
  id: any;
  date: any;
  status: string;
  connection: GetTable_workspace_table_events_data_connection;
}

export interface GetTable_workspace_table_events {
  __typename: "EventPagination";
  data: GetTable_workspace_table_events_data[];
}

export interface GetTable_workspace_table {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  metadata: any;
  columns: GetTable_workspace_table_columns;
  source_tables: GetTable_workspace_table_source_tables;
  destination_tables: GetTable_workspace_table_destination_tables;
  sources: GetTable_workspace_table_sources;
  events: GetTable_workspace_table_events;
}

export interface GetTable_workspace {
  __typename: "Workspace";
  id: any;
  table: GetTable_workspace_table;
}

export interface GetTable {
  workspace: GetTable_workspace;
}

export interface GetTableVariables {
  organisationName: string;
  workspaceName: string;
  tableId: string;
}
