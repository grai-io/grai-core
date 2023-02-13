/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspace
// ====================================================

export interface GetWorkspace_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
}

export interface GetWorkspace {
  workspace: GetWorkspace_workspace;
}

export interface GetWorkspaceVariables {
  organisationName: string;
  workspaceName: string;
}
