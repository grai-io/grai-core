/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL fragment: NewConnection
// ====================================================

export interface NewConnection_connector {
  __typename: "Connector";
  id: any;
  name: string;
}

export interface NewConnection {
  __typename: "Connection";
  id: any;
  connector: NewConnection_connector;
  namespace: string;
  name: string;
  metadata: any;
  is_active: boolean;
  created_at: any;
  updated_at: any;
}
