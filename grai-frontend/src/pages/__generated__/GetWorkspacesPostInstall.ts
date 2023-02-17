/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspacesPostInstall
// ====================================================

export interface GetWorkspacesPostInstall_workspaces_organisation {
  __typename: "Organisation";
  id: any;
  name: string;
}

export interface GetWorkspacesPostInstall_workspaces {
  __typename: "Workspace";
  id: any;
  name: string;
  organisation: GetWorkspacesPostInstall_workspaces_organisation;
}

export interface GetWorkspacesPostInstall {
  workspaces: GetWorkspacesPostInstall_workspaces[];
}
