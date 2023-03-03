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
}

export interface UpdateConnectionInitial_updateConnection {
  __typename: "Connection";
  id: any;
  connector: UpdateConnectionInitial_updateConnection_connector;
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
  namespace: string;
  name: string;
  metadata: any;
  secrets?: any | null;
}
