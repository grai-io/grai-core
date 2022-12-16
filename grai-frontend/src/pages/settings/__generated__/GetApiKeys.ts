/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetApiKeys
// ====================================================

export interface GetApiKeys_workspace_apiKeys_createdBy {
  __typename: "User";
  id: any;
  username: string | null;
}

export interface GetApiKeys_workspace_apiKeys {
  __typename: "WorkspaceAPIKey";
  id: string;
  name: string;
  prefix: string;
  created: any;
  revoked: boolean;
  expiryDate: any | null;
  createdBy: GetApiKeys_workspace_apiKeys_createdBy;
}

export interface GetApiKeys_workspace {
  __typename: "Workspace";
  id: any;
  apiKeys: GetApiKeys_workspace_apiKeys[];
}

export interface GetApiKeys {
  workspace: GetApiKeys_workspace;
}

export interface GetApiKeysVariables {
  workspaceId: string;
}
