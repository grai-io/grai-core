/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdges
// ====================================================

export interface GetTablesAndEdges_workspace_graph_columns_destinations {
  __typename: "GraphNode";
  id: string;
}

export interface GetTablesAndEdges_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  destinations: GetTablesAndEdges_workspace_graph_columns_destinations[];
}

export interface GetTablesAndEdges_workspace_graph_destinations {
  __typename: "GraphNode";
  id: string;
}

export interface GetTablesAndEdges_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  namespace: string;
  data_source: string;
  columns: GetTablesAndEdges_workspace_graph_columns[];
  destinations: GetTablesAndEdges_workspace_graph_destinations[];
}

export interface GetTablesAndEdges_workspace {
  __typename: "Workspace";
  id: any;
  graph: GetTablesAndEdges_workspace_graph[];
}

export interface GetTablesAndEdges {
  workspace: GetTablesAndEdges_workspace;
}

export interface GetTablesAndEdgesVariables {
  organisationName: string;
  workspaceName: string;
}
