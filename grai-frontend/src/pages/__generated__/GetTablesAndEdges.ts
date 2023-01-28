/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdges
// ====================================================

export interface GetTablesAndEdges_workspace_tables_columns {
  __typename: "Column";
  id: any;
  name: string;
}

export interface GetTablesAndEdges_workspace_tables {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  metadata: any;
  columns: GetTablesAndEdges_workspace_tables_columns[];
}

export interface GetTablesAndEdges_workspace_other_edges_source {
  __typename: "Node";
  id: any;
}

export interface GetTablesAndEdges_workspace_other_edges_destination {
  __typename: "Node";
  id: any;
}

export interface GetTablesAndEdges_workspace_other_edges {
  __typename: "Edge";
  id: any;
  source: GetTablesAndEdges_workspace_other_edges_source;
  destination: GetTablesAndEdges_workspace_other_edges_destination;
  metadata: any;
}

export interface GetTablesAndEdges_workspace {
  __typename: "Workspace";
  id: any;
  tables: GetTablesAndEdges_workspace_tables[];
  other_edges: GetTablesAndEdges_workspace_other_edges[];
}

export interface GetTablesAndEdges {
  workspace: GetTablesAndEdges_workspace;
}

export interface GetTablesAndEdgesVariables {
  workspaceId: string;
}
