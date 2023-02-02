/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspace
// ====================================================

export interface GetWorkspace_workspace_organisation {
  __typename: "Organisation";
  id: any;
  name: string;
}

export interface GetWorkspace_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  organisation: GetWorkspace_workspace_organisation;
}

export interface GetWorkspace {
  workspace: GetWorkspace_workspace;
}

export interface GetWorkspaceVariables {
  workspaceId: string;
}
