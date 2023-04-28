/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetFiltersControl
// ====================================================

export interface GetFiltersControl_workspace_filters_data {
  __typename: "Filter";
  id: any;
  name: string | null;
}

export interface GetFiltersControl_workspace_filters {
  __typename: "FilterPagination";
  data: GetFiltersControl_workspace_filters_data[];
}

export interface GetFiltersControl_workspace {
  __typename: "Workspace";
  id: any;
  filters: GetFiltersControl_workspace_filters;
}

export interface GetFiltersControl {
  workspace: GetFiltersControl_workspace;
}

export interface GetFiltersControlVariables {
  organisationName: string;
  workspaceName: string;
}
