/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNodes
// ====================================================

export interface GetNodes_nodes {
  __typename: "NodeType";
  id: any;
  namespace: string;
  name: string;
  displayName: string;
  isActive: boolean;
  dataSource: string;
  metadata: any;
}

export interface GetNodes {
  nodes: GetNodes_nodes[];
}
