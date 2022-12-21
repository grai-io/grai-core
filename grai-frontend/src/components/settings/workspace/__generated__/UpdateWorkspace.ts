/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateWorkspace
// ====================================================

export interface UpdateWorkspace_updateWorkspace {
  __typename: "Workspace";
  id: any;
  name: string;
}

export interface UpdateWorkspace {
  updateWorkspace: UpdateWorkspace_updateWorkspace;
}

export interface UpdateWorkspaceVariables {
  id: string;
  name: string;
}
