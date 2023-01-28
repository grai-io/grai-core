/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetTablesAndEdgesTableLineage
// ====================================================

export interface GetTablesAndEdgesTableLineage_workspace_tables {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  data_source: string;
  metadata: any;
}

export interface GetTablesAndEdgesTableLineage_workspace_edges_source {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  is_active: boolean;
  metadata: any;
}

export interface GetTablesAndEdgesTableLineage_workspace_edges_destination {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  is_active: boolean;
  metadata: any;
}

export interface GetTablesAndEdgesTableLineage_workspace_edges {
  __typename: "Edge";
  id: any;
  is_active: boolean;
  data_source: string;
  source: GetTablesAndEdgesTableLineage_workspace_edges_source;
  destination: GetTablesAndEdgesTableLineage_workspace_edges_destination;
  metadata: any;
}

export interface GetTablesAndEdgesTableLineage_workspace {
  __typename: "Workspace";
  id: any;
  tables: GetTablesAndEdgesTableLineage_workspace_tables[];
  edges: GetTablesAndEdgesTableLineage_workspace_edges[];
}

export interface GetTablesAndEdgesTableLineage {
  workspace: GetTablesAndEdgesTableLineage_workspace;
}

export interface GetTablesAndEdgesTableLineageVariables {
  workspaceId: string;
}
