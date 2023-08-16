/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceSourceGraph
// ====================================================

export interface GetWorkspaceSourceGraph_workspace_source_graph {
  __typename: "SourceGraph";
  id: any;
  name: string;
  icon: string | null;
  targets: string[];
}

export interface GetWorkspaceSourceGraph_workspace {
  __typename: "Workspace";
  id: any;
  source_graph: GetWorkspaceSourceGraph_workspace_source_graph[];
}

export interface GetWorkspaceSourceGraph {
  workspace: GetWorkspaceSourceGraph_workspace;
}

export interface GetWorkspaceSourceGraphVariables {
  workspaceId: string;
}
