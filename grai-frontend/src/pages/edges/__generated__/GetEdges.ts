/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetEdges
// ====================================================

export interface GetEdges_edges_source {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetEdges_edges_destination {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  dataSource: string;
  isActive: boolean;
  metadata: any;
}

export interface GetEdges_edges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  source: GetEdges_edges_source;
  destination: GetEdges_edges_destination;
  metadata: any;
}

export interface GetEdges {
  edges: GetEdges_edges[];
}
