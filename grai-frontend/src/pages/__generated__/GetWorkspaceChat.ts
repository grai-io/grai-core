/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceChat
// ====================================================

export interface GetWorkspaceChat_workspace {
  __typename: "Workspace";
  id: any;
}

export interface GetWorkspaceChat {
  workspace: GetWorkspaceChat_workspace;
}

export interface GetWorkspaceChatVariables {
  organisationName: string;
  workspaceName: string;
}
