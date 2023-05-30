/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdgesTableLineage
// ====================================================

export interface GetTablesAndEdgesTableLineage_workspace_tables_data_columns_data {
  __typename: "Column";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTablesAndEdgesTableLineage_workspace_tables_data_columns {
  __typename: "ColumnDataWrapper";
  data: GetTablesAndEdgesTableLineage_workspace_tables_data_columns_data[];
}

export interface GetTablesAndEdgesTableLineage_workspace_tables_data_source_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTablesAndEdgesTableLineage_workspace_tables_data_source_tables {
  __typename: "TableDataWrapper";
  data: GetTablesAndEdgesTableLineage_workspace_tables_data_source_tables_data[];
}

export interface GetTablesAndEdgesTableLineage_workspace_tables_data_destination_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTablesAndEdgesTableLineage_workspace_tables_data_destination_tables {
  __typename: "TableDataWrapper";
  data: GetTablesAndEdgesTableLineage_workspace_tables_data_destination_tables_data[];
}

export interface GetTablesAndEdgesTableLineage_workspace_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
  data_source: string;
  columns: GetTablesAndEdgesTableLineage_workspace_tables_data_columns;
  source_tables: GetTablesAndEdgesTableLineage_workspace_tables_data_source_tables;
  destination_tables: GetTablesAndEdgesTableLineage_workspace_tables_data_destination_tables;
}

export interface GetTablesAndEdgesTableLineage_workspace_tables {
  __typename: "TablePagination";
  data: GetTablesAndEdgesTableLineage_workspace_tables_data[];
}

export interface GetTablesAndEdgesTableLineage_workspace_other_edges_data_source {
  __typename: "Node";
  id: any;
}

export interface GetTablesAndEdgesTableLineage_workspace_other_edges_data_destination {
  __typename: "Node";
  id: any;
}

export interface GetTablesAndEdgesTableLineage_workspace_other_edges_data {
  __typename: "Edge";
  id: any;
  source: GetTablesAndEdgesTableLineage_workspace_other_edges_data_source;
  destination: GetTablesAndEdgesTableLineage_workspace_other_edges_data_destination;
}

export interface GetTablesAndEdgesTableLineage_workspace_other_edges {
  __typename: "EdgePagination";
  data: GetTablesAndEdgesTableLineage_workspace_other_edges_data[];
}

export interface GetTablesAndEdgesTableLineage_workspace {
  __typename: "Workspace";
  id: any;
  tables: GetTablesAndEdgesTableLineage_workspace_tables;
  other_edges: GetTablesAndEdgesTableLineage_workspace_other_edges;
}

export interface GetTablesAndEdgesTableLineage {
  workspace: GetTablesAndEdgesTableLineage_workspace;
}

export interface GetTablesAndEdgesTableLineageVariables {
  organisationName: string;
  workspaceName: string;
}
