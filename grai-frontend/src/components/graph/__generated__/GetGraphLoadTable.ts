/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetGraphLoadTable
// ====================================================

export interface GetGraphLoadTable_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  destinations: string[];
}

export interface GetGraphLoadTable_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  namespace: string;
  data_source: string;
  columns: GetGraphLoadTable_workspace_graph_columns[];
  destinations: string[];
  all_destinations: string[] | null;
  all_sources: string[] | null;
}

export interface GetGraphLoadTable_workspace {
  __typename: "Workspace";
  id: any;
  graph: GetGraphLoadTable_workspace_graph[];
}

export interface GetGraphLoadTable {
  workspace: GetGraphLoadTable_workspace;
}

export interface GetGraphLoadTableVariables {
  organisationName: string;
  workspaceName: string;
  tableId: string;
}
