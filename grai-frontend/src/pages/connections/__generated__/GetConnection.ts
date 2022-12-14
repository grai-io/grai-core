/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnection
// ====================================================

export interface GetConnection_workspace_connection_connector {
  __typename: "ConnectorType";
  id: any;
  name: string;
  metadata: any;
}

export interface GetConnection_workspace_connection {
  __typename: "ConnectionType";
  id: any;
  namespace: string;
  name: string;
  connector: GetConnection_workspace_connection_connector;
  metadata: any;
  createdAt: any;
  updatedAt: any;
}

export interface GetConnection_workspace {
  __typename: "WorkspaceType";
  id: any;
  connection: GetConnection_workspace_connection;
}

export interface GetConnection {
  workspace: GetConnection_workspace;
}

export interface GetConnectionVariables {
  workspaceId: string;
  connectionId: string;
}
