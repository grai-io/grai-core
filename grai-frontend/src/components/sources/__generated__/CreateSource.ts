/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateSource
// ====================================================

export interface CreateSource_createSource {
  __typename: "Source";
  id: any;
  name: string;
  priority: number;
}

export interface CreateSource {
  createSource: CreateSource_createSource;
}

export interface CreateSourceVariables {
  workspaceId: string;
  name: string;
  priority: number;
}
