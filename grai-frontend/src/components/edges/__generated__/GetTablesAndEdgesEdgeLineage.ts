/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdgesEdgeLineage
// ====================================================

export interface GetTablesAndEdgesEdgeLineage_workspace_tables_data_columns_data {
  __typename: "Column";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTablesAndEdgesEdgeLineage_workspace_tables_data_columns {
  __typename: "ColumnDataWrapper";
  data: GetTablesAndEdgesEdgeLineage_workspace_tables_data_columns_data[];
}

export interface GetTablesAndEdgesEdgeLineage_workspace_tables_data_source_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTablesAndEdgesEdgeLineage_workspace_tables_data_source_tables {
  __typename: "TableDataWrapper";
  data: GetTablesAndEdgesEdgeLineage_workspace_tables_data_source_tables_data[];
}

export interface GetTablesAndEdgesEdgeLineage_workspace_tables_data_destination_tables_data {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTablesAndEdgesEdgeLineage_workspace_tables_data_destination_tables {
  __typename: "TableDataWrapper";
  data: GetTablesAndEdgesEdgeLineage_workspace_tables_data_destination_tables_data[];
}

export interface GetTablesAndEdgesEdgeLineage_workspace_tables_data {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  metadata: any;
  columns: GetTablesAndEdgesEdgeLineage_workspace_tables_data_columns;
  source_tables: GetTablesAndEdgesEdgeLineage_workspace_tables_data_source_tables;
  destination_tables: GetTablesAndEdgesEdgeLineage_workspace_tables_data_destination_tables;
}

export interface GetTablesAndEdgesEdgeLineage_workspace_tables {
  __typename: "TablePagination";
  data: GetTablesAndEdgesEdgeLineage_workspace_tables_data[];
}

export interface GetTablesAndEdgesEdgeLineage_workspace_other_edges_data_source {
  __typename: "Node";
  id: any;
}

export interface GetTablesAndEdgesEdgeLineage_workspace_other_edges_data_destination {
  __typename: "Node";
  id: any;
}

export interface GetTablesAndEdgesEdgeLineage_workspace_other_edges_data {
  __typename: "Edge";
  id: any;
  source: GetTablesAndEdgesEdgeLineage_workspace_other_edges_data_source;
  destination: GetTablesAndEdgesEdgeLineage_workspace_other_edges_data_destination;
  metadata: any;
}

export interface GetTablesAndEdgesEdgeLineage_workspace_other_edges {
  __typename: "EdgePagination";
  data: GetTablesAndEdgesEdgeLineage_workspace_other_edges_data[];
}

export interface GetTablesAndEdgesEdgeLineage_workspace {
  __typename: "Workspace";
  id: any;
  tables: GetTablesAndEdgesEdgeLineage_workspace_tables;
  other_edges: GetTablesAndEdgesEdgeLineage_workspace_other_edges;
}

export interface GetTablesAndEdgesEdgeLineage {
  workspace: GetTablesAndEdgesEdgeLineage_workspace;
}

export interface GetTablesAndEdgesEdgeLineageVariables {
  organisationName: string;
  workspaceName: string;
}
