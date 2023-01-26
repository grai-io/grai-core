/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UploadDbtManifest
// ====================================================

export interface UploadDbtManifest_uploadDbtManifest {
  __typename: "BasicResult";
  success: boolean;
}

export interface UploadDbtManifest {
  uploadDbtManifest: UploadDbtManifest_uploadDbtManifest;
}

export interface UploadDbtManifestVariables {
  workspaceId: string;
  namespace: string;
  file: any;
}
