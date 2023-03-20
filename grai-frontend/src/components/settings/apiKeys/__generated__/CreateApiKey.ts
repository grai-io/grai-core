/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateApiKey
// ====================================================

export interface CreateApiKey_createApiKey_api_key {
  __typename: "WorkspaceAPIKey";
  id: string;
  /**
   * A free-form name for the API key. Need not be unique. 50 characters max.
   */
  name: string;
  /**
   * Once API key expires, clients cannot use it anymore.
   */
  expiry_date: any | null;
  /**
   * If the API key is revoked, clients cannot use it anymore. (This cannot be undone.)
   */
  revoked: boolean;
}

export interface CreateApiKey_createApiKey {
  __typename: "KeyResult";
  key: string;
  api_key: CreateApiKey_createApiKey_api_key;
}

export interface CreateApiKey {
  createApiKey: CreateApiKey_createApiKey;
}

export interface CreateApiKeyVariables {
  workspaceId: string;
  name: string;
  expiry_date?: any | null;
}
