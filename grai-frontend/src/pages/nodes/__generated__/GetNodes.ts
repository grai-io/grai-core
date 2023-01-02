/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNodes
// ====================================================

export interface GetNodes_workspace_nodes {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  data_source: string;
  metadata: any;
}

export interface GetNodes_workspace {
  __typename: "Workspace";
  id: any;
  nodes: GetNodes_workspace_nodes[];
}

export interface GetNodes {
  workspace: GetNodes_workspace;
}

export interface GetNodesVariables {
  workspaceId: string;
}
