/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

import { WorkspaceEdgeFilter } from "./../../../../__generated__/globalTypes";

// ====================================================
// GraphQL query operation: GetEdges
// ====================================================

export interface GetEdges_workspace_edges_data_source {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
}

export interface GetEdges_workspace_edges_data_destination {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
}

export interface GetEdges_workspace_edges_data {
  __typename: "Edge";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  metadata: any;
  source: GetEdges_workspace_edges_data_source;
  destination: GetEdges_workspace_edges_data_destination;
}

export interface GetEdges_workspace_edges_meta {
  __typename: "PaginationResult";
  filtered: number;
  total: number;
}

export interface GetEdges_workspace_edges {
  __typename: "EdgePagination";
  data: GetEdges_workspace_edges_data[];
  meta: GetEdges_workspace_edges_meta;
}

export interface GetEdges_workspace {
  __typename: "Workspace";
  id: any;
  edges: GetEdges_workspace_edges;
}

export interface GetEdges {
  workspace: GetEdges_workspace;
}

export interface GetEdgesVariables {
  organisationName: string;
  workspaceName: string;
  offset?: number | null;
  search?: string | null;
  filter?: WorkspaceEdgeFilter | null;
}
