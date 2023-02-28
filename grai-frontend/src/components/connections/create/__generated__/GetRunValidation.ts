/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetRunValidation
// ====================================================

export interface GetRunValidation_workspace_run {
  __typename: "Run";
  id: any;
  status: string;
}

export interface GetRunValidation_workspace {
  __typename: "Workspace";
  id: any;
  run: GetRunValidation_workspace_run;
}

export interface GetRunValidation {
  workspace: GetRunValidation_workspace;
}

export interface GetRunValidationVariables {
  workspaceId: string;
  runId: string;
}
