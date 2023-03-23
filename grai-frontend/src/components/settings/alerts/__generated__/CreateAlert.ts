/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateAlert
// ====================================================

export interface CreateAlert_createAlert {
  __typename: "Alert";
  id: any;
  name: string;
  channel: string;
  channel_metadata: any;
  triggers: any;
  is_active: boolean;
  created_at: any;
}

export interface CreateAlert {
  createAlert: CreateAlert_createAlert;
}

export interface CreateAlertVariables {
  workspaceId: string;
  name: string;
  channel: string;
  channel_metadata: any;
  triggers: any;
}
