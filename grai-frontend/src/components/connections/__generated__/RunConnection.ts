/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: RunConnection
// ====================================================

export interface RunConnection_runConnection_user {
  __typename: "User";
  id: any;
  first_name: string;
}

export interface RunConnection_runConnection {
  __typename: "Run";
  id: any;
  status: string;
  created_at: any;
  started_at: any | null;
  finished_at: any | null;
  user: RunConnection_runConnection_user | null;
}

export interface RunConnection {
  runConnection: RunConnection_runConnection;
}

export interface RunConnectionVariables {
  connectionId: string;
}
