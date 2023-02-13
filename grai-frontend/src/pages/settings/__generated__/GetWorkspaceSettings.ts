/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceSettings
// ====================================================

export interface GetWorkspaceSettings_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
}

export interface GetWorkspaceSettings {
  workspace: GetWorkspaceSettings_workspace;
}

export interface GetWorkspaceSettingsVariables {
  organisationName: string;
  workspaceName: string;
}
