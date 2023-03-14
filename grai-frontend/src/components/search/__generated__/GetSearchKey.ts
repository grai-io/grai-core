/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSearchKey
// ====================================================

export interface GetSearchKey_workspace {
  __typename: "Workspace";
  id: any;
  search_key: string;
}

export interface GetSearchKey {
  workspace: GetSearchKey_workspace;
}

export interface GetSearchKeyVariables {
  workspaceId: string;
}
