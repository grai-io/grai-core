/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateConnection
// ====================================================

export interface UpdateConnection_updateConnection {
  __typename: "ConnectionType";
  id: any;
  namespace: string;
  name: string;
  metadata: any;
  isActive: boolean;
  createdAt: any;
  updatedAt: any;
}

export interface UpdateConnection {
  updateConnection: UpdateConnection_updateConnection;
}

export interface UpdateConnectionVariables {
  connectionId: string;
  namespace: string;
  name: string;
  metadata: any;
  secrets: any;
}
