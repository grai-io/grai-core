/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAlert
// ====================================================

export interface GetAlert_workspace_alert {
  __typename: "Alert";
  id: any;
  name: string;
  channel: string;
  channel_metadata: any;
  triggers: any;
  is_active: boolean;
  created_at: any;
}

export interface GetAlert_workspace {
  __typename: "Workspace";
  id: any;
  alert: GetAlert_workspace_alert;
}

export interface GetAlert {
  workspace: GetAlert_workspace;
}

export interface GetAlertVariables {
  organisationName: string;
  workspaceName: string;
  id: string;
}
