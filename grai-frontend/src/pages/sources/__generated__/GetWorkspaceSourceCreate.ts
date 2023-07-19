/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceSourceCreate
// ====================================================

export interface GetWorkspaceSourceCreate_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
}

export interface GetWorkspaceSourceCreate {
  workspace: GetWorkspaceSourceCreate_workspace;
}

export interface GetWorkspaceSourceCreateVariables {
  organisationName: string;
  workspaceName: string;
}
