/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetFiltersDrawer
// ====================================================

export interface GetFiltersDrawer_workspace_filters_data {
  __typename: "Filter";
  id: any;
  name: string | null;
}

export interface GetFiltersDrawer_workspace_filters {
  __typename: "FilterPagination";
  data: GetFiltersDrawer_workspace_filters_data[];
}

export interface GetFiltersDrawer_workspace {
  __typename: "Workspace";
  id: any;
  filters: GetFiltersDrawer_workspace_filters;
}

export interface GetFiltersDrawer {
  workspace: GetFiltersDrawer_workspace;
}

export interface GetFiltersDrawerVariables {
  organisationName: string;
  workspaceName: string;
  search?: string | null;
}
