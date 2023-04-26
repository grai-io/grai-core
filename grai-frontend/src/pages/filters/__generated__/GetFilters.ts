/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetFilters
// ====================================================

export interface GetFilters_workspace_filters_data {
  __typename: "Filter";
  id: any;
  name: string | null;
  created_at: any;
}

export interface GetFilters_workspace_filters_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetFilters_workspace_filters {
  __typename: "FilterPagination";
  data: GetFilters_workspace_filters_data[];
  meta: GetFilters_workspace_filters_meta;
}

export interface GetFilters_workspace {
  __typename: "Workspace";
  id: any;
  filters: GetFilters_workspace_filters;
}

export interface GetFilters {
  workspace: GetFilters_workspace;
}

export interface GetFiltersVariables {
  organisationName: string;
  workspaceName: string;
}
