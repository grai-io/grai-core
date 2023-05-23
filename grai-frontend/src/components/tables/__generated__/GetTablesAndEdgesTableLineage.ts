/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdgesTableLineage
// ====================================================

export interface GetTablesAndEdgesTableLineage_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  destinations: string[];
}

export interface GetTablesAndEdgesTableLineage_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  namespace: string;
  data_source: string;
  columns: GetTablesAndEdgesTableLineage_workspace_graph_columns[];
  destinations: string[];
  all_destinations: string[] | null;
  all_sources: string[] | null;
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
