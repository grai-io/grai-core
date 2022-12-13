/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnection
// ====================================================

export interface GetConnection_connection_connector {
  __typename: "ConnectorType";
  id: any;
  name: string;
  metadata: any;
}

export interface GetConnection_connection {
  __typename: "ConnectionType";
  id: any;
  namespace: string;
  name: string;
  connector: GetConnection_connection_connector;
  metadata: any;
  createdAt: any;
  updatedAt: any;
}

export interface GetConnection {
  connection: GetConnection_connection;
}

export interface GetConnectionVariables {
  connectionId: string;
}
