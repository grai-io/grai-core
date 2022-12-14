/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnections
// ====================================================

export interface GetConnections_workspace_connections_connector {
  __typename: "ConnectorType";
  id: any;
  name: string;
}

export interface GetConnections_workspace_connections {
  __typename: "ConnectionType";
  id: any;
  namespace: string;
  name: string;
  connector: GetConnections_workspace_connections_connector;
}

export interface GetConnections_workspace {
  __typename: "WorkspaceType";
  connections: GetConnections_workspace_connections[];
}

export interface GetConnections {
  workspace: GetConnections_workspace;
}

export interface GetConnectionsVariables {
  workspaceId: string;
}
