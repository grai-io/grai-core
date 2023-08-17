/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceFilterInline
// ====================================================

export interface GetWorkspaceFilterInline_workspace_namespaces {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetWorkspaceFilterInline_workspace_tags {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetWorkspaceFilterInline_workspace_sources_data {
  __typename: "Source";
  id: any;
  name: string;
}

export interface GetWorkspaceFilterInline_workspace_sources {
  __typename: "SourcePagination";
  data: GetWorkspaceFilterInline_workspace_sources_data[];
}

export interface GetWorkspaceFilterInline_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  namespaces: GetWorkspaceFilterInline_workspace_namespaces;
  tags: GetWorkspaceFilterInline_workspace_tags;
  sources: GetWorkspaceFilterInline_workspace_sources;
}

export interface GetWorkspaceFilterInline {
  workspace: GetWorkspaceFilterInline_workspace;
}

export interface GetWorkspaceFilterInlineVariables {
  workspaceId: string;
}
