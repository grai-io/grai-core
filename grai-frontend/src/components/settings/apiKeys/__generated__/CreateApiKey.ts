/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateApiKey
// ====================================================

export interface CreateApiKey_createApiKey_apiKey {
  __typename: "WorkspaceAPIKey";
  id: string;
  name: string;
}

export interface CreateApiKey_createApiKey {
  __typename: "KeyResult";
  key: string;
  apiKey: CreateApiKey_createApiKey_apiKey;
}

export interface CreateApiKey {
  createApiKey: CreateApiKey_createApiKey;
}

export interface CreateApiKeyVariables {
  name: string;
  workspaceId: string;
}
