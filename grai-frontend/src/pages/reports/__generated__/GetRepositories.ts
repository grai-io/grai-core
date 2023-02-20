/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRepositories
// ====================================================

export interface GetRepositories_workspace_repositories {
  __typename: "Repository";
  id: any;
  type: string;
  owner: string;
  repo: string;
}

export interface GetRepositories_workspace {
  __typename: "Workspace";
  id: any;
  repositories: GetRepositories_workspace_repositories[];
}

export interface GetRepositories {
  workspace: GetRepositories_workspace;
}

export interface GetRepositoriesVariables {
  organisationName: string;
  workspaceName: string;
  type: string;
  owner: string;
}
