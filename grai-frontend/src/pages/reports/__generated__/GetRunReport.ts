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
  status: string;
  metadata: any;
  created_at: any;
  commit: GetRunReport_workspace_run_commit | null;
}

export interface GetRunReport_workspace_graph_columns {
  __typename: "GraphColumn";
  id: string;
  name: string;
  display_name: string;
  destinations: string[];
}

export interface GetRunReport_workspace_graph {
  __typename: "GraphTable";
  id: string;
  name: string;
  display_name: string;
  namespace: string;
  data_source: string;
  columns: GetRunReport_workspace_graph_columns[];
  destinations: string[];
}

export interface GetRunReport_workspace {
  __typename: "Workspace";
  id: any;
  run: GetRunReport_workspace_run;
  graph: GetRunReport_workspace_graph[];
}

export interface GetRunReport {
  workspace: GetRunReport_workspace;
}

export interface GetRunReportVariables {
  organisationName: string;
  workspaceName: string;
  runId: string;
}
