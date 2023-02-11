/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateWorkspace
// ====================================================

export interface CreateWorkspace_createWorkspace_organisation {
  __typename: "Organisation";
  id: any;
  name: string;
}

export interface CreateWorkspace_createWorkspace {
  __typename: "Workspace";
  id: any;
  name: string;
  organisation: CreateWorkspace_createWorkspace_organisation;
}

export interface CreateWorkspace {
  createWorkspace: CreateWorkspace_createWorkspace;
}

export interface CreateWorkspaceVariables {
  organisationName: string;
  name: string;
}
