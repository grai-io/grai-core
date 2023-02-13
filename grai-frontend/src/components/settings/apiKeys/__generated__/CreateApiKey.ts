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
  name: string;
  workspaceId: string;
}
