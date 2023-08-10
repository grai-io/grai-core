/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceSourceGraph
// ====================================================

export interface GetWorkspaceSourceGraph_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  source_graph: any;
}

export interface GetWorkspaceSourceGraph {
  workspace: GetWorkspaceSourceGraph_workspace;
}

export interface GetWorkspaceSourceGraphVariables {
  organisationName: string;
  workspaceName: string;
}
