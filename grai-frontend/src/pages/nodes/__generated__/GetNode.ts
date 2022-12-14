/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNode
// ====================================================

export interface GetNode_workspace_node_sourceEdges_destination {
  __typename: "NodeType";
  id: any;
  name: string;
  displayName: string;
  metadata: any;
}

export interface GetNode_workspace_node_sourceEdges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  destination: GetNode_workspace_node_sourceEdges_destination;
  metadata: any;
}

export interface GetNode_workspace_node_destinationEdges_source {
  __typename: "NodeType";
  id: any;
  name: string;
  displayName: string;
  metadata: any;
}

export interface GetNode_workspace_node_destinationEdges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  source: GetNode_workspace_node_destinationEdges_source;
  metadata: any;
}

export interface GetNode_workspace_node {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  isActive: boolean;
  dataSource: string;
  sourceEdges: GetNode_workspace_node_sourceEdges[];
  destinationEdges: GetNode_workspace_node_destinationEdges[];
  metadata: any;
}

export interface GetNode_workspace_nodes {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  isActive: boolean;
  dataSource: string;
  metadata: any;
}

export interface GetNode_workspace_edges_source {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetNode_workspace_edges_destination {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetNode_workspace_edges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  source: GetNode_workspace_edges_source;
  destination: GetNode_workspace_edges_destination;
  metadata: any;
}

export interface GetNode_workspace {
  __typename: "WorkspaceType";
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
