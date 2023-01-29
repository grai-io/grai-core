/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaces
// ====================================================

export interface GetWorkspaces_workspaces_organisation {
  __typename: "Organisation";
  id: any;
  name: string;
}

export interface GetWorkspaces_workspaces {
  __typename: "Workspace";
  id: any;
  name: string;
  organisation: GetWorkspaces_workspaces_organisation;
}

export interface GetWorkspaces {
  workspaces: GetWorkspaces_workspaces[];
}
