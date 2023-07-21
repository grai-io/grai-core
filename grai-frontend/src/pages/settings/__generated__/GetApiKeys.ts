/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetApiKeys
// ====================================================

export interface GetApiKeys_workspace_api_keys_data_created_by {
  __typename: "User";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface GetApiKeys_workspace_api_keys_data {
  __typename: "WorkspaceAPIKey";
  id: string;
  name: string;
  prefix: string;
  created: any;
  revoked: boolean;
  expiry_date: any | null;
  created_by: GetApiKeys_workspace_api_keys_data_created_by;
}

export interface GetApiKeys_workspace_api_keys {
  __typename: "WorkspaceAPIKeyPagination";
  data: GetApiKeys_workspace_api_keys_data[];
}

export interface GetApiKeys_workspace {
  __typename: "Workspace";
  id: any;
  api_keys: GetApiKeys_workspace_api_keys;
}

export interface GetApiKeys {
  workspace: GetApiKeys_workspace;
}

export interface GetApiKeysVariables {
  organisationName: string;
  workspaceName: string;
}
