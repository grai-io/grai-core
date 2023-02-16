/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UploadConnectorFile
// ====================================================

export interface UploadConnectorFile_uploadConnectorFile_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
}

export interface UploadConnectorFile_uploadConnectorFile_connection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: UploadConnectorFile_uploadConnectorFile_connection_connector;
}

export interface UploadConnectorFile_uploadConnectorFile_user {
  __typename: "User";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface UploadConnectorFile_uploadConnectorFile {
  __typename: "Run";
  id: any;
  connection: UploadConnectorFile_uploadConnectorFile_connection;
  status: string;
  metadata: any;
  created_at: any;
  updated_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: UploadConnectorFile_uploadConnectorFile_user | null;
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
