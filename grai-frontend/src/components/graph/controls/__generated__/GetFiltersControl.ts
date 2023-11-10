/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetFiltersControl
// ====================================================

export interface GetFiltersControl_workspace_namespaces {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetFiltersControl_workspace_tags {
  __typename: "StrDataWrapper";
  data: string[];
}

export interface GetFiltersControl_workspace_sources_data {
  __typename: "Source";
  id: any;
  name: string;
}

export interface GetFiltersControl_workspace_sources {
  __typename: "SourcePagination";
  data: GetFiltersControl_workspace_sources_data[];
}

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
  name: string;
  namespaces: GetFiltersControl_workspace_namespaces;
  tags: GetFiltersControl_workspace_tags;
  sources: GetFiltersControl_workspace_sources;
  filters: GetFiltersControl_workspace_filters;
}

export interface GetFiltersControl {
  workspace: GetFiltersControl_workspace;
}

export interface GetFiltersControlVariables {
  organisationName: string;
  workspaceName: string;
}
