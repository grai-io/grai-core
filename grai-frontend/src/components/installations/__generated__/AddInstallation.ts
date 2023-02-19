/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: AddInstallation
// ====================================================

export interface AddInstallation_addInstallation {
  __typename: "BasicResult";
  success: boolean;
}

export interface AddInstallation {
  addInstallation: AddInstallation_addInstallation;
}

export interface AddInstallationVariables {
  workspaceId: string;
  installationId: number;
}
