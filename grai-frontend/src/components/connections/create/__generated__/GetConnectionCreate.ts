/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetConnectionCreate
// ====================================================

export interface GetConnectionCreate_workspace_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
  metadata: any;
}

export interface GetConnectionCreate_workspace_connection_source {
  __typename: "Source";
  id: any;
  name: string;
}

export interface GetConnectionCreate_workspace_connection_last_run {
  __typename: "Run";
  id: any;
  status: string;
}

export interface GetConnectionCreate_workspace_connection {
  __typename: "Connection";
  id: any;
  connector: GetConnectionCreate_workspace_connection_connector;
  source: GetConnectionCreate_workspace_connection_source;
  last_run: GetConnectionCreate_workspace_connection_last_run | null;
  namespace: string;
  name: string;
  metadata: any;
  is_active: boolean;
  created_at: any;
  updated_at: any;
}

export interface GetConnectionCreate_workspace {
  __typename: "Workspace";
  id: any;
  connection: GetConnectionCreate_workspace_connection;
}

export interface GetConnectionCreate {
  workspace: GetConnectionCreate_workspace;
}

export interface GetConnectionCreateVariables {
  workspaceId: string;
  connectionId: string;
}
