/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetAlerts
// ====================================================

export interface GetAlerts_workspace_alerts_data {
  __typename: "Alert";
  id: any;
  name: string;
  channel: string;
  channel_metadata: any;
  triggers: any;
  is_active: boolean;
  created_at: any;
}

export interface GetAlerts_workspace_alerts {
  __typename: "AlertPagination";
  data: GetAlerts_workspace_alerts_data[];
}

export interface GetAlerts_workspace {
  __typename: "Workspace";
  id: any;
  alerts: GetAlerts_workspace_alerts;
}

export interface GetAlerts {
  workspace: GetAlerts_workspace;
}

export interface GetAlertsVariables {
  organisationName: string;
  workspaceName: string;
}
