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
  display_name: string;
  is_active: boolean;
  data_source: string;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_workspace_edges_source {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  is_active: boolean;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_workspace_edges_destination {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  is_active: boolean;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_workspace_edges {
  __typename: "Edge";
  id: any;
  is_active: boolean;
  data_source: string;
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
  organisationName: string;
  workspaceName: string;
}
