/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNodesAndEdges
// ====================================================

export interface GetNodesAndEdges_nodes {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  isActive: boolean;
  dataSource: string;
  metadata: any;
}

export interface GetNodesAndEdges_edges_source {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetNodesAndEdges_edges_destination {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetNodesAndEdges_edges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  source: GetNodesAndEdges_edges_source;
  destination: GetNodesAndEdges_edges_destination;
  metadata: any;
}

export interface GetNodesAndEdges {
  nodes: GetNodesAndEdges_nodes[];
  edges: GetNodesAndEdges_edges[];
}
