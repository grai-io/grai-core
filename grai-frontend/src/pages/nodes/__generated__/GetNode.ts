/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetNode
// ====================================================

export interface GetNode_workspace_node_columns_data_requirements_edges_data_destination {
  __typename: "Node";
  id: any;
  name: string;
  display_name: string;
  metadata: any;
}

export interface GetNode_workspace_node_columns_data_requirements_edges_data {
  __typename: "Edge";
  id: any;
  metadata: any;
  destination: GetNode_workspace_node_columns_data_requirements_edges_data_destination;
}

export interface GetNode_workspace_node_columns_data_requirements_edges {
  __typename: "EdgePagination";
  data: GetNode_workspace_node_columns_data_requirements_edges_data[];
}

export interface GetNode_workspace_node_columns_data {
  __typename: "Column";
  id: any;
  name: string;
  display_name: string;
  requirements_edges: GetNode_workspace_node_columns_data_requirements_edges;
  metadata: any;
}

export interface GetNode_workspace_node_columns {
  __typename: "ColumnDataWrapper";
  data: GetNode_workspace_node_columns_data[];
}

export interface GetNode_workspace_node_data_sources_data_connections_data_connector {
  __typename: "Connector";
  id: any;
  name: string;
  slug: string | null;
}

export interface GetNode_workspace_node_data_sources_data_connections_data {
  __typename: "Connection";
  id: any;
  connector: GetNode_workspace_node_data_sources_data_connections_data_connector;
}

export interface GetNode_workspace_node_data_sources_data_connections {
  __typename: "ConnectionPagination";
  data: GetNode_workspace_node_data_sources_data_connections_data[];
}

export interface GetNode_workspace_node_data_sources_data {
  __typename: "Source";
  id: any;
  name: string;
  connections: GetNode_workspace_node_data_sources_data_connections;
}

export interface GetNode_workspace_node_data_sources {
  __typename: "SourcePagination";
  data: GetNode_workspace_node_data_sources_data[];
}

export interface GetNode_workspace_node_events_data_connection_connector {
  __typename: "Connector";
  id: any;
  name: string;
}

export interface GetNode_workspace_node_events_data_connection {
  __typename: "Connection";
  id: any;
  name: string;
  connector: GetNode_workspace_node_events_data_connection_connector;
}

export interface GetNode_workspace_node_events_data {
  __typename: "Event";
  id: any;
  date: any;
  status: string;
  connection: GetNode_workspace_node_events_data_connection;
}

export interface GetNode_workspace_node_events {
  __typename: "EventPagination";
  data: GetNode_workspace_node_events_data[];
}

export interface GetNode_workspace_node {
  __typename: "Node";
  id: any;
  namespace: string;
  name: string;
  display_name: string;
  is_active: boolean;
  metadata: any;
  columns: GetNode_workspace_node_columns;
  data_sources: GetNode_workspace_node_data_sources;
  events: GetNode_workspace_node_events;
}

export interface GetNode_workspace {
  __typename: "Workspace";
  id: any;
  node: GetNode_workspace_node;
}

export interface GetNode {
  workspace: GetNode_workspace;
}

export interface GetNodeVariables {
  organisationName: string;
  workspaceName: string;
  nodeId: string;
}
