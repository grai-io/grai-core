/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL fragment: NewSourceConnection
// ====================================================

export interface NewSourceConnection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
}

export interface NewSourceConnection_last_run {
  __typename: "Run";
  id: any;
  status: string;
}

export interface NewSourceConnection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: NewSourceConnection_connector;
  last_run: NewSourceConnection_last_run | null;
}
