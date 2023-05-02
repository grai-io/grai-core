/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRepositoriesGitHubInstallation
// ====================================================

export interface GetRepositoriesGitHubInstallation_workspace_repositories_data {
  __typename: "Repository";
  id: any;
  owner: string;
  repo: string;
}

export interface GetRepositoriesGitHubInstallation_workspace_repositories {
  __typename: "RepositoryPagination";
  data: GetRepositoriesGitHubInstallation_workspace_repositories_data[];
}

export interface GetRepositoriesGitHubInstallation_workspace {
  __typename: "Workspace";
  id: any;
  repositories: GetRepositoriesGitHubInstallation_workspace_repositories;
}

export interface GetRepositoriesGitHubInstallation {
  workspace: GetRepositoriesGitHubInstallation_workspace;
}

export interface GetRepositoriesGitHubInstallationVariables {
  organisationName: string;
  workspaceName: string;
}
