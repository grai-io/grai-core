/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetEdges
// ====================================================

export interface GetEdges_workspace_edges_source {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetEdges_workspace_edges_destination {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetEdges_workspace_edges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  source: GetEdges_workspace_edges_source;
  destination: GetEdges_workspace_edges_destination;
  metadata: any;
}

export interface GetEdges_workspace {
  __typename: "WorkspaceType";
  id: any;
  edges: GetEdges_workspace_edges[];
}

export interface GetEdges {
  workspace: GetEdges_workspace;
}

export interface GetEdgesVariables {
  workspaceId: string;
}
