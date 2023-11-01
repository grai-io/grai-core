/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateWorkspaceSampleData
// ====================================================

export interface UpdateWorkspaceSampleData_updateWorkspace {
  __typename: "Workspace";
  id: any;
  sample_data: boolean;
}

export interface UpdateWorkspaceSampleData {
  updateWorkspace: UpdateWorkspaceSampleData_updateWorkspace;
}

export interface UpdateWorkspaceSampleDataVariables {
  id: string;
}
