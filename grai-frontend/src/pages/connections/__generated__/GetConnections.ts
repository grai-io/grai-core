/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnections
// ====================================================

export interface GetConnections_connections_connector {
  __typename: "ConnectorType";
  id: any;
  name: string;
}

export interface GetConnections_connections {
  __typename: "ConnectionType";
  id: any;
  namespace: string;
  name: string;
  connector: GetConnections_connections_connector;
}

export interface GetConnections {
  connections: GetConnections_connections[];
}
