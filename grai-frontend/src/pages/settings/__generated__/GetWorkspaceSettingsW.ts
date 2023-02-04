/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceSettingsW
// ====================================================

export interface GetWorkspaceSettingsW_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
}

export interface GetWorkspaceSettingsW {
  workspace: GetWorkspaceSettingsW_workspace;
}

export interface GetWorkspaceSettingsWVariables {
  organisationName: string;
  workspaceName: string;
}
