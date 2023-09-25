/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateConnectionInitial
// ====================================================

export interface UpdateConnectionInitial_updateConnection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
}

export interface UpdateConnectionInitial_updateConnection_source {
  __typename: "Source";
  id: any;
  name: string;
  priority: number;
}

export interface UpdateConnectionInitial_updateConnection_last_run {
  __typename: "Run";
  id: any;
  status: string;
}

export interface UpdateConnectionInitial_updateConnection {
  __typename: "Connection";
  id: any;
  connector: UpdateConnectionInitial_updateConnection_connector;
  source: UpdateConnectionInitial_updateConnection_source;
  last_run: UpdateConnectionInitial_updateConnection_last_run | null;
  namespace: string;
  name: string;
  metadata: any;
  created_at: any;
  updated_at: any;
}

export interface UpdateConnectionInitial {
  updateConnection: UpdateConnectionInitial_updateConnection;
}

export interface UpdateConnectionInitialVariables {
  connectionId: string;
  sourceName: string;
  namespace: string;
  name: string;
  metadata: any;
  secrets?: any | null;
}
