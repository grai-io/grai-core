/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnectionSchedule
// ====================================================

export interface GetConnectionSchedule_workspace_connection_connector {
  __typename: "Connector";
  id: any;
  slug: string | null;
  name: string;
  icon: string | null;
  metadata: any;
}

export interface GetConnectionSchedule_workspace_connection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: GetConnectionSchedule_workspace_connection_connector;
  metadata: any;
}

export interface GetConnectionSchedule_workspace {
  __typename: "Workspace";
  id: any;
  connection: GetConnectionSchedule_workspace_connection;
}

export interface GetConnectionSchedule {
  workspace: GetConnectionSchedule_workspace;
}

export interface GetConnectionScheduleVariables {
  workspaceId: string;
  connectionId: string;
}
