/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdgesEdgeLineage
// ====================================================

export interface GetTablesAndEdgesEdgeLineage_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  destinations: string[];
}

export interface GetTablesAndEdgesEdgeLineage_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  namespace: string;
  data_source: string;
  columns: GetTablesAndEdgesEdgeLineage_workspace_graph_columns[];
  destinations: string[];
  all_destinations: string[] | null;
  all_sources: string[] | null;
}

export interface GetTablesAndEdgesEdgeLineage_workspace {
  __typename: "Workspace";
  id: any;
  graph: GetTablesAndEdgesEdgeLineage_workspace_graph[];
}

export interface GetTablesAndEdgesEdgeLineage {
  workspace: GetTablesAndEdgesEdgeLineage_workspace;
}

export interface GetTablesAndEdgesEdgeLineageVariables {
  organisationName: string;
  workspaceName: string;
  edgeId: string;
  n: number;
}
