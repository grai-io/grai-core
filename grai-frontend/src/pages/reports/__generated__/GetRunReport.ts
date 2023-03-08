/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRunReport
// ====================================================

export interface GetRunReport_workspace_run_commit_branch {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetRunReport_workspace_run_commit_pull_request {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
}

export interface GetRunReport_workspace_run_commit_repository {
  __typename: "Repository";
  id: any;
  type: string;
  owner: string;
  repo: string;
}

export interface GetRunReport_workspace_run_commit {
  __typename: "Commit";
  id: any;
  reference: string;
  branch: GetRunReport_workspace_run_commit_branch;
  pull_request: GetRunReport_workspace_run_commit_pull_request | null;
  repository: GetRunReport_workspace_run_commit_repository;
}

export interface GetRunReport_workspace_run {
  __typename: "Run";
  id: any;
  metadata: any;
  created_at: any;
  commit: GetRunReport_workspace_run_commit | null;
}

export interface GetRunReport_workspace_tables_columns {
  __typename: "Column";
  id: any;
  name: string;
}

export interface GetRunReport_workspace_tables_source_tables {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetRunReport_workspace_tables_destination_tables {
  __typename: "Table";
  id: any;
  name: string;
  display_name: string;
}

export interface GetRunReport_workspace_tables {
  __typename: "Table";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  data_source: string;
  metadata: any;
  columns: GetRunReport_workspace_tables_columns[];
  source_tables: GetRunReport_workspace_tables_source_tables[];
  destination_tables: GetRunReport_workspace_tables_destination_tables[];
}

export interface GetRunReport_workspace_other_edges_source {
  __typename: "Node";
  id: any;
}

export interface GetRunReport_workspace_other_edges_destination {
  __typename: "Node";
  id: any;
}

export interface GetRunReport_workspace_other_edges {
  __typename: "Edge";
  id: any;
  source: GetRunReport_workspace_other_edges_source;
  destination: GetRunReport_workspace_other_edges_destination;
  metadata: any;
}

export interface GetRunReport_workspace {
  __typename: "Workspace";
  id: any;
  run: GetRunReport_workspace_run;
  tables: GetRunReport_workspace_tables[];
  other_edges: GetRunReport_workspace_other_edges[];
}

export interface GetRunReport {
  workspace: GetRunReport_workspace;
}

export interface GetRunReportVariables {
  organisationName: string;
  workspaceName: string;
  runId: string;
}
