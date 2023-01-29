/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceConnectionCreate
// ====================================================

export interface GetWorkspaceConnectionCreate_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
}

export interface GetWorkspaceConnectionCreate {
  workspace: GetWorkspaceConnectionCreate_workspace;
}

export interface GetWorkspaceConnectionCreateVariables {
  organisationName: string;
  workspaceName: string;
}
