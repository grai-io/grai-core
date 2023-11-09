/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceProvider
// ====================================================

export interface GetWorkspaceProvider_workspace_organisation {
  __typename: "Organisation";
  id: any;
}

export interface GetWorkspaceProvider_workspace_runs_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetWorkspaceProvider_workspace_runs {
  __typename: "RunPagination";
  meta: GetWorkspaceProvider_workspace_runs_meta;
}

export interface GetWorkspaceProvider_workspace_nodes_meta {
  __typename: "PaginationResult";
  filtered: number;
}

export interface GetWorkspaceProvider_workspace_nodes {
  __typename: "NodePagination";
  meta: GetWorkspaceProvider_workspace_nodes_meta;
}

export interface GetWorkspaceProvider_workspace_connections_meta {
  __typename: "PaginationResult";
  total: number;
}

export interface GetWorkspaceProvider_workspace_connections {
  __typename: "ConnectionPagination";
  meta: GetWorkspaceProvider_workspace_connections_meta;
}

export interface GetWorkspaceProvider_workspace_last_chat_messages_data {
  __typename: "Message";
  id: any;
  message: string;
  role: string;
  created_at: any;
}

export interface GetWorkspaceProvider_workspace_last_chat_messages {
  __typename: "MessagePagination";
  data: GetWorkspaceProvider_workspace_last_chat_messages_data[];
}

export interface GetWorkspaceProvider_workspace_last_chat {
  __typename: "Chat";
  id: any;
  messages: GetWorkspaceProvider_workspace_last_chat_messages;
}

export interface GetWorkspaceProvider_workspace {
  __typename: "Workspace";
  id: any;
  name: string;
  sample_data: boolean;
  organisation: GetWorkspaceProvider_workspace_organisation;
  runs: GetWorkspaceProvider_workspace_runs;
  nodes: GetWorkspaceProvider_workspace_nodes;
  connections: GetWorkspaceProvider_workspace_connections;
  last_chat: GetWorkspaceProvider_workspace_last_chat;
}

export interface GetWorkspaceProvider_profile {
  __typename: "Profile";
  id: any;
  username: string | null;
  first_name: string;
  last_name: string;
}

export interface GetWorkspaceProvider {
  workspace: GetWorkspaceProvider_workspace;
  profile: GetWorkspaceProvider_profile;
}

export interface GetWorkspaceProviderVariables {
  organisationName: string;
  workspaceName: string;
}
