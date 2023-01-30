/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspacesIndex
// ====================================================

export interface GetWorkspacesIndex_workspaces_organisation {
  __typename: "Organisation";
  id: any;
  name: string;
}

export interface GetWorkspacesIndex_workspaces {
  __typename: "Workspace";
  id: any;
  name: string;
  organisation: GetWorkspacesIndex_workspaces_organisation;
}

export interface GetWorkspacesIndex {
  workspaces: GetWorkspacesIndex_workspaces[];
}
