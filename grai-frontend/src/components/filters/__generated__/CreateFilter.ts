/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateFilter
// ====================================================

export interface CreateFilter_createFilter {
  __typename: "Filter";
  id: any;
  name: string | null;
  metadata: any;
  created_at: any;
}

export interface CreateFilter {
  createFilter: CreateFilter_createFilter;
}

export interface CreateFilterVariables {
  workspaceId: string;
  name: string;
  metadata: any;
}
