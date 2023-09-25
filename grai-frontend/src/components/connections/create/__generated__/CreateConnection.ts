/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateConnection
// ====================================================

export interface CreateConnection_createConnection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
}

export interface CreateConnection_createConnection_source {
  __typename: "Source";
  id: any;
  name: string;
}

export interface CreateConnection_createConnection_last_run {
  __typename: "Run";
  id: any;
  status: string;
}

export interface CreateConnection_createConnection {
  __typename: "Connection";
  id: any;
  connector: CreateConnection_createConnection_connector;
  source: CreateConnection_createConnection_source;
  last_run: CreateConnection_createConnection_last_run | null;
  namespace: string;
  name: string;
  metadata: any;
  is_active: boolean;
  created_at: any;
  updated_at: any;
}

export interface CreateConnection {
  createConnection: CreateConnection_createConnection;
}

export interface CreateConnectionVariables {
  workspaceId: string;
  connectorId: string;
  sourceName: string;
  namespace: string;
  name: string;
  metadata: any;
  secrets?: any | null;
}
