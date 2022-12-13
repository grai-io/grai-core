/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNodesAndEdgesNodeLineage
// ====================================================

export interface GetNodesAndEdgesNodeLineage_nodes {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  isActive: boolean;
  dataSource: string;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_edges_source {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_edges_destination {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage_edges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  source: GetNodesAndEdgesNodeLineage_edges_source;
  destination: GetNodesAndEdgesNodeLineage_edges_destination;
  metadata: any;
}

export interface GetNodesAndEdgesNodeLineage {
  nodes: GetNodesAndEdgesNodeLineage_nodes[];
  edges: GetNodesAndEdgesNodeLineage_edges[];
}
