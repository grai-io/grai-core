/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: SearchGraphTables
// ====================================================

export interface SearchGraphTables_workspace_graph_tables {
  __typename: "BaseGraph";
  id: string;
  name: string;
  display_name: string;
  data_source: string;
  x: number;
  y: number;
}

export interface SearchGraphTables_workspace {
  __typename: "Workspace";
  id: any;
  graph_tables: SearchGraphTables_workspace_graph_tables[];
}

export interface SearchGraphTables {
  workspace: SearchGraphTables_workspace;
}

export interface SearchGraphTablesVariables {
  organisationName: string;
  workspaceName: string;
  search?: string | null;
}
