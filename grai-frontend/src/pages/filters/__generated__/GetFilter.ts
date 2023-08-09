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

export interface GetFilter_workspace_namespaces {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetFilter_workspace_tags {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetFilter_workspace_sources_data {
  __typename: "Source";
  id: any;
  name: string;
}

export interface GetFilter_workspace_sources {
  __typename: "SourcePagination";
  data: GetFilter_workspace_sources_data[];
}

export interface GetFilter_workspace {
  __typename: "Workspace";
  id: any;
  filter: GetFilter_workspace_filter;
  namespaces: GetFilter_workspace_namespaces;
  tags: GetFilter_workspace_tags;
  sources: GetFilter_workspace_sources;
}

export interface GetFilter {
  workspace: GetFilter_workspace;
}

export interface GetFilterVariables {
  organisationName: string;
  workspaceName: string;
  filterId: string;
}
