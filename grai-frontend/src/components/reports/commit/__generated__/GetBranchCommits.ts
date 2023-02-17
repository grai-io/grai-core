/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetBranchCommits
// ====================================================

export interface GetBranchCommits_workspace_repository_branch_commits_last_successful_run {
  __typename: "Run";
  id: any;
  metadata: any;
}

export interface GetBranchCommits_workspace_repository_branch_commits_branch {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetBranchCommits_workspace_repository_branch_commits_pull_request {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
}

export interface GetBranchCommits_workspace_repository_branch_commits {
  __typename: "Commit";
  id: any;
  reference: string;
  title: string | null;
  created_at: any;
  last_successful_run: GetBranchCommits_workspace_repository_branch_commits_last_successful_run | null;
  branch: GetBranchCommits_workspace_repository_branch_commits_branch;
  pull_request: GetBranchCommits_workspace_repository_branch_commits_pull_request | null;
}

export interface GetBranchCommits_workspace_repository_branch {
  __typename: "Branch";
  id: any;
  commits: GetBranchCommits_workspace_repository_branch_commits[];
}

export interface GetBranchCommits_workspace_repository {
  __typename: "Repository";
  id: any;
  owner: string;
  repo: string;
  branch: GetBranchCommits_workspace_repository_branch;
}

export interface GetBranchCommits_workspace {
  __typename: "Workspace";
  id: any;
  repository: GetBranchCommits_workspace_repository;
}

export interface GetBranchCommits {
  workspace: GetBranchCommits_workspace;
}

export interface GetBranchCommitsVariables {
  organisationName: string;
  workspaceName: string;
  type: string;
  owner: string;
  repo: string;
  reference: string;
}
