/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceFilterCreate
// ====================================================

export interface GetWorkspaceFilterCreate_workspace_tags {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetWorkspaceFilterCreate_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  tags: GetWorkspaceFilterCreate_workspace_tags;
}

export interface GetWorkspaceFilterCreate {
  workspace: GetWorkspaceFilterCreate_workspace;
}

export interface GetWorkspaceFilterCreateVariables {
  organisationName: string;
  workspaceName: string;
}
