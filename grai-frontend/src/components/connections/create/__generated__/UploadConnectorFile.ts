/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UploadConnectorFile
// ====================================================

export interface UploadConnectorFile_uploadConnectorFile {
  __typename: "BasicResult";
  success: boolean;
}

export interface UploadConnectorFile {
  uploadConnectorFile: UploadConnectorFile_uploadConnectorFile;
}

export interface UploadConnectorFileVariables {
  workspaceId: string;
  connectorId: string;
  namespace: string;
  file: any;
}
