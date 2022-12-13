/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNode
// ====================================================

export interface GetNode_node_sourceEdges_destination {
  __typename: "NodeType";
  id: any;
  name: string;
  displayName: string;
  metadata: any;
}

export interface GetNode_node_sourceEdges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  destination: GetNode_node_sourceEdges_destination;
  metadata: any;
}

export interface GetNode_node_destinationEdges_source {
  __typename: "NodeType";
  id: any;
  name: string;
  displayName: string;
  metadata: any;
}

export interface GetNode_node_destinationEdges {
  __typename: "EdgeType";
  id: any;
  isActive: boolean;
  dataSource: string;
  source: GetNode_node_destinationEdges_source;
  metadata: any;
}

export interface GetNode_node {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  isActive: boolean;
  dataSource: string;
  sourceEdges: GetNode_node_sourceEdges[];
  destinationEdges: GetNode_node_destinationEdges[];
  metadata: any;
}

export interface GetNode {
  node: GetNode_node;
}

export interface GetNodeVariables {
  nodeId: string;
}
