/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: LoadWorkspaceSampleData
// ====================================================

export interface LoadWorkspaceSampleData_loadWorkspaceSampleData_organisation {
  __typename: "Organisation";
  id: any;
  name: string;
}

export interface LoadWorkspaceSampleData_loadWorkspaceSampleData {
  __typename: "Workspace";
  id: any;
  name: string;
  organisation: LoadWorkspaceSampleData_loadWorkspaceSampleData_organisation;
}

export interface LoadWorkspaceSampleData {
  loadWorkspaceSampleData: LoadWorkspaceSampleData_loadWorkspaceSampleData;
}

export interface LoadWorkspaceSampleDataVariables {
  id: string;
}
