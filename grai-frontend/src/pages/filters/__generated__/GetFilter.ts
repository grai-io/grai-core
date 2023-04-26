/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetFilter
// ====================================================

export interface GetFilter_workspace_filter {
  __typename: "Filter";
  id: any;
  name: string | null;
  metadata: any;
  created_at: any;
}

export interface GetFilter_workspace {
  __typename: "Workspace";
  id: any;
  filter: GetFilter_workspace_filter;
}

export interface GetFilter {
  workspace: GetFilter_workspace;
}

export interface GetFilterVariables {
  organisationName: string;
  workspaceName: string;
  filterId: string;
}
