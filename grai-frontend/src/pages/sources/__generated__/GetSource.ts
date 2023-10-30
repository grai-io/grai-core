/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetSource
// ====================================================

export interface GetSource_workspace_source_connections_data_connector {
  __typename: "Connector";
  id: any;
  name: string;
  icon: string | null;
}

export interface GetSource_workspace_source_connections_data_last_run {
  __typename: "Run";
  id: any;
  status: string;
}

export interface GetSource_workspace_source_connections_data {
  __typename: "Connection";
  id: any;
  name: string;
  validated: boolean;
  connector: GetSource_workspace_source_connections_data_connector;
  last_run: GetSource_workspace_source_connections_data_last_run | null;
}

export interface GetSource_workspace_source_connections {
  __typename: "ConnectionPagination";
  data: GetSource_workspace_source_connections_data[];
}

export interface GetSource_workspace_source {
  __typename: "Source";
  id: any;
  name: string;
  priority: number;
  connections: GetSource_workspace_source_connections;
}

export interface GetSource_workspace {
  __typename: "Workspace";
  id: any;
  source: GetSource_workspace_source;
}

export interface GetSource {
  workspace: GetSource_workspace;
}

export interface GetSourceVariables {
  organisationName: string;
  workspaceName: string;
  sourceId: string;
}
