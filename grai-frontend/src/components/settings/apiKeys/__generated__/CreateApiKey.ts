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
  name: string;
  expiry_date: any | null;
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
