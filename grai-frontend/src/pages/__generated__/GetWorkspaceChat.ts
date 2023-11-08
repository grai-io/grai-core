/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: GetWorkspaceChat
// ====================================================

export interface GetWorkspaceChat_workspace_last_chat_messages_data {
  __typename: "Message";
  id: any;
  message: string;
  role: string;
  created_at: any;
}

export interface GetWorkspaceChat_workspace_last_chat_messages {
  __typename: "MessagePagination";
  data: GetWorkspaceChat_workspace_last_chat_messages_data[];
}

export interface GetWorkspaceChat_workspace_last_chat {
  __typename: "Chat";
  id: any;
  messages: GetWorkspaceChat_workspace_last_chat_messages;
}

export interface GetWorkspaceChat_workspace {
  __typename: "Workspace";
  id: any;
  last_chat: GetWorkspaceChat_workspace_last_chat;
}

export interface GetWorkspaceChat {
  workspace: GetWorkspaceChat_workspace;
}

export interface GetWorkspaceChatVariables {
  organisationName: string;
  workspaceName: string;
}
