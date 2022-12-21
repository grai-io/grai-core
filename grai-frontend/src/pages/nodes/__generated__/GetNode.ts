/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNode
// ====================================================

export interface GetNode_workspace_node {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  data_source: string;
  metadata: any;
}

export interface GetNode_workspace_nodes {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  data_source: string;
  metadata: any;
}

export interface GetNode_workspace_edges_source {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  is_active: boolean;
  metadata: any;
}

export interface GetNode_workspace_edges_destination {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  is_active: boolean;
  metadata: any;
}

export interface GetNode_workspace_edges {
  __typename: "Edge";
  id: any;
  is_active: boolean;
  data_source: string;
  source: GetNode_workspace_edges_source;
  destination: GetNode_workspace_edges_destination;
  metadata: any;
}

export interface GetNode_workspace {
  __typename: "Workspace";
  id: any;
  node: GetNode_workspace_node;
  nodes: GetNode_workspace_nodes[];
  edges: GetNode_workspace_edges[];
}

export interface GetNode {
  workspace: GetNode_workspace;
}

export interface GetNodeVariables {
  workspaceId: string;
  nodeId: string;
}
