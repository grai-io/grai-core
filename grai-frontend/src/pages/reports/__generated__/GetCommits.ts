/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetCommits
// ====================================================

export interface GetCommits_workspace_repository_commits_last_successful_run {
  __typename: "Run";
  id: any;
  metadata: any;
}

export interface GetCommits_workspace_repository_commits_branch {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetCommits_workspace_repository_commits_pull_request {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
}

export interface GetCommits_workspace_repository_commits {
  __typename: "Commit";
  id: any;
  reference: string;
  title: string | null;
  created_at: any;
  last_successful_run: GetCommits_workspace_repository_commits_last_successful_run | null;
  branch: GetCommits_workspace_repository_commits_branch;
  pull_request: GetCommits_workspace_repository_commits_pull_request | null;
}

export interface GetCommits_workspace_repository_branches {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetCommits_workspace_repository {
  __typename: "Repository";
  id: any;
  owner: string;
  repo: string;
  commits: GetCommits_workspace_repository_commits[];
  branches: GetCommits_workspace_repository_branches[];
}

export interface GetCommits_workspace {
  __typename: "Workspace";
  id: any;
  repository: GetCommits_workspace_repository;
}

export interface GetCommits {
  workspace: GetCommits_workspace;
}

export interface GetCommitsVariables {
  organisationName: string;
  workspaceName: string;
  type: string;
  owner: string;
  repo: string;
}
