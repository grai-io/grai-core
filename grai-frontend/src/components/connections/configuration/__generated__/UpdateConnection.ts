/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: UpdateConnection
// ====================================================

export interface UpdateConnection_updateConnection {
  __typename: "Connection";
  id: any;
  namespace: string;
  name: string;
  metadata: any;
  is_active: boolean;
  created_at: any;
  updated_at: any;
}

export interface UpdateConnection {
  updateConnection: UpdateConnection_updateConnection;
}

export interface UpdateConnectionVariables {
  connectionId: string;
  namespace: string;
  name: string;
  metadata: any;
  secrets?: any | null;
  schedules?: any | null;
  is_active?: boolean | null;
}
