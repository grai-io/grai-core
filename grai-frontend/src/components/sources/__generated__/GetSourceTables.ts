/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSourceTables
// ====================================================

export interface GetSourceTables_workspace_source_nodes_data {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
}

export interface GetSourceTables_workspace_source_nodes {
  __typename: "NodePagination";
  data: GetSourceTables_workspace_source_nodes_data[];
}

export interface GetSourceTables_workspace_source {
  __typename: "Source";
  id: any;
  nodes: GetSourceTables_workspace_source_nodes;
}

export interface GetSourceTables_workspace {
  __typename: "Workspace";
  id: any;
  source: GetSourceTables_workspace_source;
}

export interface GetSourceTables {
  workspace: GetSourceTables_workspace;
}

export interface GetSourceTablesVariables {
  workspaceId: string;
  sourceId: string;
}
