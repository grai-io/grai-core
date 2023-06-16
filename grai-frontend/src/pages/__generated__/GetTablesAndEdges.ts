/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { GraphFilter } from "./../../../__generated__/globalTypes";

// ====================================================
// GraphQL query operation: GetTablesAndEdges
// ====================================================

export interface GetTablesAndEdges_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  display_name: string;
  destinations: string[];
}

export interface GetTablesAndEdges_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  display_name: string;
  namespace: string;
  data_source: string;
  x: number;
  y: number;
  columns: GetTablesAndEdges_workspace_graph_columns[];
  destinations: string[];
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
  filters?: GraphFilter | null;
}
