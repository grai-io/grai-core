/* tslint:disable */
/* eslint-disable */
// @generated
// This file was automatically generated and should not be edited.

// ====================================================
// GraphQL mutation operation: CreateChat
// ====================================================

export interface CreateChat_createChat_messages_data {
  __typename: "Message";
  id: any;
  message: string;
  role: string;
  created_at: any;
}

export interface CreateChat_createChat_messages {
  __typename: "MessagePagination";
  data: CreateChat_createChat_messages_data[];
}

export interface CreateChat_createChat {
  __typename: "Chat";
  id: any;
  messages: CreateChat_createChat_messages;
}

export interface CreateChat {
  createChat: CreateChat_createChat;
}

export interface CreateChatVariables {
  workspaceId: string;
}
