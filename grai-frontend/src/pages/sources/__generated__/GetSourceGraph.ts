/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSourceGraph
// ====================================================

export interface GetSourceGraph_workspace_source_graph {
  __typename: "SourceGraph";
  id: any;
  name: string;
  icon: string | null;
  targets: string[];
}

export interface GetSourceGraph_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  source_graph: GetSourceGraph_workspace_source_graph[];
}

export interface GetSourceGraph {
  workspace: GetSourceGraph_workspace;
}

export interface GetSourceGraphVariables {
  organisationName: string;
  workspaceName: string;
}
