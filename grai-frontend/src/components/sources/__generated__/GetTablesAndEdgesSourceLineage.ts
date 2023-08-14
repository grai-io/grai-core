/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdgesSourceLineage
// ====================================================

export interface GetTablesAndEdgesSourceLineage_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  display_name: string;
  destinations: string[];
}

export interface GetTablesAndEdgesSourceLineage_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  display_name: string;
  namespace: string;
  x: number;
  y: number;
  data_source: string | null;
  columns: GetTablesAndEdgesSourceLineage_workspace_graph_columns[];
  destinations: string[];
  table_destinations: string[] | null;
  table_sources: string[] | null;
}

export interface GetTablesAndEdgesSourceLineage_workspace {
  __typename: "Workspace";
  id: any;
  graph: GetTablesAndEdgesSourceLineage_workspace_graph[];
}

export interface GetTablesAndEdgesSourceLineage {
  workspace: GetTablesAndEdgesSourceLineage_workspace;
}

export interface GetTablesAndEdgesSourceLineageVariables {
  organisationName: string;
  workspaceName: string;
  sourceId: string;
  n: number;
}
