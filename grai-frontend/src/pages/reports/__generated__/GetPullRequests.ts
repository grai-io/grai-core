/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetPullRequests
// ====================================================

export interface GetPullRequests_workspace_repository_pull_requests_last_commit_last_successful_run {
  __typename: "Run";
  id: any;
  metadata: any;
}

export interface GetPullRequests_workspace_repository_pull_requests_last_commit {
  __typename: "Commit";
  id: any;
  reference: string;
  created_at: any;
  last_successful_run: GetPullRequests_workspace_repository_pull_requests_last_commit_last_successful_run | null;
}

export interface GetPullRequests_workspace_repository_pull_requests_branch {
  __typename: "Branch";
  id: any;
  reference: string;
}

export interface GetPullRequests_workspace_repository_pull_requests {
  __typename: "PullRequest";
  id: any;
  reference: string;
  title: string | null;
  last_commit: GetPullRequests_workspace_repository_pull_requests_last_commit | null;
  branch: GetPullRequests_workspace_repository_pull_requests_branch;
}

export interface GetPullRequests_workspace_repository {
  __typename: "Repository";
  id: any;
  owner: string;
  repo: string;
  pull_requests: GetPullRequests_workspace_repository_pull_requests[];
}

export interface GetPullRequests_workspace {
  __typename: "Workspace";
  id: any;
  repository: GetPullRequests_workspace_repository;
}

export interface GetPullRequests {
  workspace: GetPullRequests_workspace;
}

export interface GetPullRequestsVariables {
  organisationName: string;
  workspaceName: string;
  type: string;
  owner: string;
  repo: string;
}
