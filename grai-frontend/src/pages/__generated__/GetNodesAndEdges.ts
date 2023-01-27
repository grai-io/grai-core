/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNodesAndEdges
// ====================================================

export interface GetNodesAndEdges_workspace_nodes {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  metadata: any;
}

export interface GetNodesAndEdges_workspace_edges_source {
  __typename: "Node";
  id: any;
}

export interface GetNodesAndEdges_workspace_edges_destination {
  __typename: "Node";
  id: any;
}

export interface GetNodesAndEdges_workspace_edges {
  __typename: "Edge";
  id: any;
  source: GetNodesAndEdges_workspace_edges_source;
  destination: GetNodesAndEdges_workspace_edges_destination;
  metadata: any;
}

export interface GetNodesAndEdges_workspace {
  __typename: "Workspace";
  id: any;
  nodes: GetNodesAndEdges_workspace_nodes[];
  edges: GetNodesAndEdges_workspace_edges[];
}

export interface GetNodesAndEdges {
  workspace: GetNodesAndEdges_workspace;
}

export interface GetNodesAndEdgesVariables {
  workspaceId: string;
}
