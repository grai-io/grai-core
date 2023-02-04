/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceHome
// ====================================================

export interface GetWorkspaceHome_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
}

export interface GetWorkspaceHome {
  workspace: GetWorkspaceHome_workspace;
}

export interface GetWorkspaceHomeVariables {
  organisationName: string;
  workspaceName: string;
}
