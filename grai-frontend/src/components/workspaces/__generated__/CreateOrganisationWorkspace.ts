/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateOrganisationWorkspace
// ====================================================

export interface CreateOrganisationWorkspace_createWorkspace_organisation {
  __typename: "Organisation";
  id: any;
  name: string;
}

export interface CreateOrganisationWorkspace_createWorkspace {
  __typename: "Workspace";
  id: any;
  name: string;
  organisation: CreateOrganisationWorkspace_createWorkspace_organisation;
}

export interface CreateOrganisationWorkspace {
  createWorkspace: CreateOrganisationWorkspace_createWorkspace;
}

export interface CreateOrganisationWorkspaceVariables {
  organisationId: string;
  name: string;
}
