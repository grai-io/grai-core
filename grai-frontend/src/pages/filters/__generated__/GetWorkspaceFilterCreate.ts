/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceFilterCreate
// ====================================================

export interface GetWorkspaceFilterCreate_workspace_namespaces {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetWorkspaceFilterCreate_workspace_tags {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetWorkspaceFilterCreate_workspace_sources_data {
  __typename: "Source";
  id: any;
  name: string;
}

export interface GetWorkspaceFilterCreate_workspace_sources {
  __typename: "SourcePagination";
  data: GetWorkspaceFilterCreate_workspace_sources_data[];
}

export interface GetWorkspaceFilterCreate_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  namespaces: GetWorkspaceFilterCreate_workspace_namespaces;
  tags: GetWorkspaceFilterCreate_workspace_tags;
  sources: GetWorkspaceFilterCreate_workspace_sources;
}

export interface GetWorkspaceFilterCreate {
  workspace: GetWorkspaceFilterCreate_workspace;
}

export interface GetWorkspaceFilterCreateVariables {
  organisationName: string;
  workspaceName: string;
}
