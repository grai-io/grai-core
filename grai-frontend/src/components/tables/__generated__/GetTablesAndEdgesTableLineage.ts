/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdgesTableLineage
// ====================================================

export interface GetTablesAndEdgesTableLineage_workspace_graph_columns_destinations {
  __typename: "ColumnEdge";
  edge_id: string;
  column_id: string;
}

export interface GetTablesAndEdgesTableLineage_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  display_name: string;
  destinations: GetTablesAndEdgesTableLineage_workspace_graph_columns_destinations[];
}

export interface GetTablesAndEdgesTableLineage_workspace_graph_destinations {
  __typename: "TableEdge";
  edge_id: string;
  table_id: string;
}

export interface GetTablesAndEdgesTableLineage_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  display_name: string;
  namespace: string;
  x: number;
  y: number;
  data_source: string | null;
  columns: GetTablesAndEdgesTableLineage_workspace_graph_columns[];
  destinations: GetTablesAndEdgesTableLineage_workspace_graph_destinations[];
  table_destinations: string[] | null;
  table_sources: string[] | null;
}

export interface GetTablesAndEdgesTableLineage_workspace {
  __typename: "Workspace";
  id: any;
  graph: GetTablesAndEdgesTableLineage_workspace_graph[];
}

export interface GetTablesAndEdgesTableLineage {
  workspace: GetTablesAndEdgesTableLineage_workspace;
}

export interface GetTablesAndEdgesTableLineageVariables {
  organisationName: string;
  workspaceName: string;
  tableId: string;
  n: number;
}
