/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateFilterInline
// ====================================================

export interface CreateFilterInline_createFilter {
  __typename: "Filter";
  id: any;
  name: string | null;
  metadata: any;
  created_at: any;
}

export interface CreateFilterInline {
  createFilter: CreateFilterInline_createFilter;
}

export interface CreateFilterInlineVariables {
  workspaceId: string;
  name: string;
  metadata: any;
}
