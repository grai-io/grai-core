/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL query operation: LastChat
// ====================================================

export interface LastChat_workspace_last_chat_messages_data {
  __typename: "Message";
  id: any;
  message: string;
  role: string;
  created_at: any;
}

export interface LastChat_workspace_last_chat_messages {
  __typename: "MessagePagination";
  data: LastChat_workspace_last_chat_messages_data[];
}

export interface LastChat_workspace_last_chat {
  __typename: "Chat";
  id: any;
  messages: LastChat_workspace_last_chat_messages;
}

export interface LastChat_workspace {
  __typename: "Workspace";
  id: any;
  last_chat: LastChat_workspace_last_chat;
}

export interface LastChat {
  workspace: LastChat_workspace;
}

export interface LastChatVariables {
  workspaceId: string;
}
