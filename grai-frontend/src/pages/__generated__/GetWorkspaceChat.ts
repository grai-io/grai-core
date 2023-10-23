/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceChat
// ====================================================

export interface GetWorkspaceChat_workspace_chats_data_messages_data {
  __typename: "Message";
  id: any;
  message: string;
  role: string;
  created_at: any;
}

export interface GetWorkspaceChat_workspace_chats_data_messages {
  __typename: "MessagePagination";
  data: GetWorkspaceChat_workspace_chats_data_messages_data[];
}

export interface GetWorkspaceChat_workspace_chats_data {
  __typename: "Chat";
  id: any;
  messages: GetWorkspaceChat_workspace_chats_data_messages;
}

export interface GetWorkspaceChat_workspace_chats {
  __typename: "ChatPagination";
  data: GetWorkspaceChat_workspace_chats_data[];
}

export interface GetWorkspaceChat_workspace {
  __typename: "Workspace";
  id: any;
  chats: GetWorkspaceChat_workspace_chats;
}

export interface GetWorkspaceChat {
  workspace: GetWorkspaceChat_workspace;
}

export interface GetWorkspaceChatVariables {
  organisationName: string;
  workspaceName: string;
}
