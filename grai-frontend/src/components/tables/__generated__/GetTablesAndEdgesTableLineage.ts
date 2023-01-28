/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdgesTableLineage
// ====================================================

export interface GetTablesAndEdgesTableLineage_workspace_tables_columns {
  __typename: "Column";
  id: any;
  name: string;
  display_name: string;
}

export interface GetTablesAndEdgesTableLineage_workspace_tables {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  metadata: any;
  columns: GetTablesAndEdgesTableLineage_workspace_tables_columns[];
}

export interface GetTablesAndEdgesTableLineage_workspace_other_edges_source {
  __typename: "Node";
  id: any;
}

export interface GetTablesAndEdgesTableLineage_workspace_other_edges_destination {
  __typename: "Node";
  id: any;
}

export interface GetTablesAndEdgesTableLineage_workspace_other_edges {
  __typename: "Edge";
  id: any;
  source: GetTablesAndEdgesTableLineage_workspace_other_edges_source;
  destination: GetTablesAndEdgesTableLineage_workspace_other_edges_destination;
  metadata: any;
}

export interface GetTablesAndEdgesTableLineage_workspace {
  __typename: "Workspace";
  id: any;
  tables: GetTablesAndEdgesTableLineage_workspace_tables[];
  other_edges: GetTablesAndEdgesTableLineage_workspace_other_edges[];
}

export interface GetTablesAndEdgesTableLineage {
  workspace: GetTablesAndEdgesTableLineage_workspace;
}

export interface GetTablesAndEdgesTableLineageVariables {
  workspaceId: string;
}
