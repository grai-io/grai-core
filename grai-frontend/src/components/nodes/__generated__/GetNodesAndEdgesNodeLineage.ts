/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNodesAndEdgesNodeLineage
// ====================================================

export interface GetNodesAndEdgesNodeLineage_workspace_nodes {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  isActive: boolean;
  dataSource: string;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_workspace_edges_source {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_workspace_edges_destination {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_workspace_edges {
  __typename: "Edge";
  id: any;
  isActive: boolean;
  dataSource: string;
  source: GetNodesAndEdgesNodeLineage_workspace_edges_source;
  destination: GetNodesAndEdgesNodeLineage_workspace_edges_destination;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_workspace {
  __typename: "Workspace";
  id: any;
  nodes: GetNodesAndEdgesNodeLineage_workspace_nodes[];
  edges: GetNodesAndEdgesNodeLineage_workspace_edges[];
}

export interface GetNodesAndEdgesNodeLineage {
  workspace: GetNodesAndEdgesNodeLineage_workspace;
}

export interface GetNodesAndEdgesNodeLineageVariables {
  workspaceId: string;
}
